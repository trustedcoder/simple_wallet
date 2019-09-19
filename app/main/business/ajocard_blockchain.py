from peewee import *
from datetime import datetime
import hashlib
import json
from app.main import config

db = SqliteDatabase('secure_wallet.db')
# channel used to tell where the fund is from
class Chain(Model):
    previous_hash = CharField()
    sender = CharField()
    receiver = CharField()
    amount = IntegerField()
    channel = IntegerField()
    proof = CharField()
    pending_date = DateTimeField()
    date_created = DateTimeField()


    class Meta:
        database = db # This model uses the "secure_fund.db" database.


class AjoCardChain(object):

    def __init__(self):
        db.connect()
        db.create_tables([Chain])
        # Create the genesis block
        if len(Chain.select()) <= 0:
            start_date = datetime.utcnow()
            chain_bob = Chain(previous_hash=1, sender='ajocard_admin1', receiver='ajocard_admin2', amount=2000000000, channel=0, proof=0, pending_date=start_date, date_created=start_date)
            chain_bob.save()

    def valid_chain(self):
        chain_list = Chain.select()
        first_index = 0
        first_block = chain_list[first_index]
        second_index = 1

        while second_index < len(chain_list):
            second_block = chain_list[second_index]
            # Check that the hash of the block is correct
            if second_block.previous_hash != self.hash(first_block):
                return False

            first_block = second_block
            second_index += 1
        return True

    def check_balance(self,address):
        total_amount_received = 0
        total_amount_sent = 0
        chain_list = Chain.select()

        for block in chain_list:
            if address == block.receiver:
                if datetime.utcnow() > block.pending_date:
                    total_amount_received = total_amount_received + block.amount
            elif address == block.sender:
                total_amount_sent = total_amount_sent + block.amount

        balance = total_amount_received - total_amount_sent
        return balance

    def valid_transaction(self,sender,amount):
        total_amount_received = 0
        total_amount_sent = 0
        chain_list = Chain.select()

        for block in chain_list:
            if sender == block.receiver:
                if datetime.utcnow() > block.pending_date:
                    total_amount_received = total_amount_received + block.amount
            elif sender == block.sender:
                total_amount_sent = total_amount_sent + block.amount

        balance = total_amount_received - total_amount_sent
        if balance < amount:
            return False
        else:
            return True

    def transaction_history(self,address):
        chain_list = Chain.select()

        history_list = []
        for block in chain_list:
            is_credited = False
            found_address = False
            the_other_user = ''
            if address == block.receiver:
                is_credited = True
                found_address = True
                the_other_user = block.sender
            elif address == block.sender:
                found_address = True
                the_other_user = block.receiver
            if found_address:
                history_list.append({
                    'is_credited': is_credited,
                    'amount': block.amount,
                    'partner': the_other_user,
                    'date': block.date_created
                })
        return history_list

    def new_block(self, sender, receiver, amount,channel,proof,date,pending_date):
        chain_list = Chain.select()

        if self.valid_transaction(sender,amount):
            if self.valid_chain():
                chain_bob = Chain(previous_hash=self.hash(chain_list[-1]), sender=sender, receiver=receiver,amount=amount, channel=channel, proof=proof, pending_date=pending_date,date_created=date)
                chain_bob.save()
                return True
            else:
                return False
        else:
            #For when app is first run
            if len(chain_list) == 0:
                chain_bob = Chain(previous_hash=self.hash(chain_list[-1]), sender=sender, receiver=receiver,amount=amount, channel=channel, proof=proof, pending_date=pending_date, date_created=date)
                chain_bob.save()
                return True
            else:
                return False

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """
        dict_string = {
            'id': block.id,
            'previous_hash':block.previous_hash,
            'sender': block.sender,
            'receiver': block.receiver,
            'amount': block.amount,
            'channel': block.channel,
            'proof': block.proof,
            'pending_date': str(block.pending_date),
            'date_created': str(block.date_created)
        }
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(dict_string, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return Chain.select()[-1]