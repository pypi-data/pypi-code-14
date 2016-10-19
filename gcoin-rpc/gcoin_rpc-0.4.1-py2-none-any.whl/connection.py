# Copyright (c) 2010 Witchspace <witchspace81@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
Connect to Bitcoin server via JSON-RPC.
"""
from gcoinrpc.proxy import AuthServiceProxy
from gcoinrpc.exceptions import (wrap_exception, BitcoinException,
                                   WalletPassphraseIncorrect,
                                   WalletAlreadyUnlocked)
from gcoinrpc.data import (ServerInfo, AccountInfo, AddressInfo, TransactionInfo,
                             AddressValidation, WorkItem, MiningInfo)


class BitcoinConnection(object):
    """
    A BitcoinConnection object defines a connection to a bitcoin server.
    It is a thin wrapper around a JSON-RPC API connection.

    Arguments to constructor:

    - *user* -- Authenticate as user.
    - *password* -- Authentication password.
    - *host* -- Bitcoin JSON-RPC host.
    - *port* -- Bitcoin JSON-RPC port.
    """
    def __init__(self, user, password, host='localhost', port=8332,
                 use_https=False):
        """
        Create a new bitcoin server connection.
        """
        url = 'http{s}://{user}:{password}@{host}:{port}/'.format(
            s='s' if use_https else '',
            user=user, password=password, host=host, port=port)
        self.url = url
        self.proxy = AuthServiceProxy(url, exception_wrapper=wrap_exception)

    def stop(self):
        """
        Stop bitcoin server.
        """
        self.proxy.stop()

    def getrtts(self, since, until, unit, node_addr=None):
        """
        Returns the total rtt to all nodes.
        """
        if node_addr is None:
            return self.proxy.getrtts(int(since), int(until), int(unit))
        else:
            return self.proxy.getrtts(int(since), int(until), int(unit), int(node_addr))

    def gettotalbandwidth(self, since, until, unit, node_addr=None):
        """
        Returns the total outbandwidth to all nodes.
        """
        if node_addr is None:
            return self.proxy.gettotalbandwidth(int(since), int(until), int(unit))
        else:
            return self.proxy.gettotalbandwidth(int(since), int(until), int(unit), int(node_addr))

    def getblock(self, hash):
        """
        Returns information about the given block hash.
        """
        return self.proxy.getblock(hash)

    def getbestblockhash(self):
        return self.proxy.getbestblockhash()

    def getblockcount(self):
        """
        Returns the number of blocks in the longest block chain.
        """
        return self.proxy.getblockcount()

    def getblockhash(self, index):
        """
        Returns hash of block in best-block-chain at index.

        :param index: index ob the block

        """
        return self.proxy.getblockhash(index)

    def getblocknumber(self):
        """
        Returns the block number of the latest block in the longest block chain.
        Deprecated. Use getblockcount instead.
        """
        return self.getblockcount()

    def getconnectioncount(self):
        """
        Returns the number of connections to other nodes.
        """
        return self.proxy.getconnectioncount()

    def getdifficulty(self):
        """
        Returns the proof-of-work difficulty as a multiple of the minimum difficulty.
        """
        return self.proxy.getdifficulty()

    def getgenerate(self):
        """
        Returns :const:`True` or :const:`False`, depending on whether generation is enabled.
        """
        return self.proxy.getgenerate()

    def setgenerate(self, generate, genproclimit=None):
        """
        Enable or disable generation (mining) of coins.

        Arguments:

        - *generate* -- is :const:`True` or :const:`False` to turn generation on or off.
        - *genproclimit* -- Number of processors that are used for generation, -1 is unlimited.

        """
        if genproclimit is None:
            return self.proxy.setgenerate(generate)
        else:
            return self.proxy.setgenerate(generate, genproclimit)

    def gethashespersec(self):
        """
        Returns a recent hashes per second performance measurement while generating.
        """
        return self.proxy.gethashespersec()

    def getinfo(self):
        """
        Returns an :class:`~gcoinrpc.data.ServerInfo` object containing various state info.
        """
        return ServerInfo(**self.proxy.getinfo())

    def getmininginfo(self):
        """
        Returns an :class:`~gcoinrpc.data.MiningInfo` object containing various
        mining state info.
        """
        return MiningInfo(**self.proxy.getmininginfo())

    def gennewaddress(self, number=1):
        """
        Generate and return new Bitcoin address for receiving payments.

        Arguments:

        - *number* -- The number of address to be fetched from the keypool.

        warn:
            Using gennewaddress RPC, user should backup wallet.dat manually.
            To utilize the keypool mechanism, you should use getnewaddressamount RPC.

        """
        return self.proxy.gennewaddress(number)

    def getnewaddress(self, account=None):
        """
        Returns a new bitcoin address for receiving payments.

        Arguments:

        - *account* -- If account is specified (recommended), it is added to the address book
          so that payments received with the address will be credited to it.

        """
        if account is None:
            return self.proxy.getnewaddress()
        else:
            return self.proxy.getnewaddress(account)

    def getnewaddressamount(self, number=1, account=None):
        """
        Fetch and returns new bitcoin address from keypool for receiving payments.

        Arguments:

        - *number* -- The number of address to be fetched from the keypool.
        - *account* -- If account is specified (recommended), it is added to the address book
          so that payments received with the address will be credited to it.

        """
        if account is None:
            return self.proxy.getnewaddressamount(number)
        else:
            return self.proxy.getnewaddressamount(number, account)

    def getaccountaddress(self, account):
        """
        Returns the current bitcoin address for receiving payments to an account.

        Arguments:

        - *account* -- Account for which the address should be returned.

        """
        return self.proxy.getaccountaddress(account)

    def setaccount(self, bitcoinaddress, account):
        """
        Sets the account associated with the given address.

        Arguments:

        - *bitcoinaddress* -- Bitcoin address to associate.
        - *account* -- Account to associate the address to.

        """
        return self.proxy.setaccount(bitcoinaddress, account)

    def getaccount(self, bitcoinaddress):
        """
        Returns the account associated with the given address.

        Arguments:

        - *bitcoinaddress* -- Bitcoin address to get account for.
        """
        return self.proxy.getaccount(bitcoinaddress)

    def getaddressesbyaccount(self, account):
        """
        Returns the list of addresses for the given account.

        Arguments:

        - *account* -- Account to get list of addresses for.
        """
        return self.proxy.getaddressesbyaccount(account)

    def sendtoaddress(self, bitcoinaddress, amount, color, comment=None, comment_to=None):
        """
        Sends *amount* from the server's available balance to *bitcoinaddress*.

        Arguments:

        - *bitcoinaddress* -- Bitcoin address to send to.
        - *amount* -- Amount to send (float, rounded to the nearest 0.00000001).
        - *color* -- Color id
        - *minconf* -- Minimum number of confirmations required for transferred balance.
        - *comment* -- Comment for transaction.
        - *comment_to* -- Comment for to-address.

        """
        if comment is None:
            return self.proxy.sendtoaddress(bitcoinaddress, amount, color)
        elif comment_to is None:
            return self.proxy.sendtoaddress(bitcoinaddress, amount, color, comment)
        else:
            return self.proxy.sendtoaddress(bitcoinaddress, amount, color, comment, comment_to)

    def getreceivedbyaddress(self, bitcoinaddress, minconf=1):
        """
        Returns the total amount received by a bitcoin address in transactions with at least a
        certain number of confirmations.

        Arguments:

        - *bitcoinaddress* -- Address to query for total amount.

        - *minconf* -- Number of confirmations to require, defaults to 1.
        """
        return self.proxy.getreceivedbyaddress(bitcoinaddress, minconf)

    def getreceivedbyaccount(self, account, minconf=1):
        """
        Returns the total amount received by addresses with an account in transactions with
        at least a certain number of confirmations.

        Arguments:

        - *account* -- Account to query for total amount.
        - *minconf* -- Number of confirmations to require, defaults to 1.

        """
        return self.proxy.getreceivedbyaccount(account, minconf)

    def gettransaction(self, txid):
        """
        Get detailed information about transaction

        Arguments:

        - *txid* -- Transactiond id for which the info should be returned

        """
        return TransactionInfo(**self.proxy.gettransaction(txid))

    def getrawtransaction(self, txid, verbose=True):
        """
        Get transaction raw info

        Arguments:

        - *txid* -- Transactiond id for which the info should be returned.
        - *verbose* -- If False, return only the "hex" of the transaction.

        """
        if verbose:
            return TransactionInfo(**self.proxy.getrawtransaction(txid, 1))
        return self.proxy.getrawtransaction(txid, 0)

    def getrawmempool(self, verbose=False):
        """
        Returns all transaction identifiers (TXIDs) in the memory pool as a JSON array,
        or detailed information about each transaction in the memory pool as a JSON object.

        Arguments:

        - *verbose* -- Set to true to get verbose output describing each transaction in the memory pool;
                       set to false (the default) to only get an array of TXIDs for transactions in the memory pool
        """
        if verbose:
            return self.proxy.getrawmempool(True)
        return self.proxy.getrawmempool(False)

    def getaddrmempool(self, bitcoinaddress, verbose=False):
        """
        Returns all transaction identifiers (TXIDs) in the memory pool which is related to a specific address
        as a JSON array, or detailed information about each transaction in the memory pool as a JSON object.

        Arguments:

        - *bitcoinaddress* -- Address to query for all transaction in the memory pool.
        - *verbose* -- Set to true to get verbose output describing each transaction in the memory pool;
                       set to false (the default) to only get an array of TXIDs for transactions in the memory pool
        """
        if verbose:
            return self.proxy.getaddrmempool(bitcoinaddress, True)
        return self.proxy.getaddrmempool(bitcoinaddress, False)

    def gettxout(self, txid, index, mempool=True):
        """
        Returns details about an unspent transaction output (UTXO)

        Arguments:

        - *txid* -- Transactiond id for which the info should be returned.
        - *index* -- The output index.
        - *mempool* -- Add memory pool transactions.
        """
        tx = self.proxy.gettxout(txid, index, mempool)
        if tx != None:
            return TransactionInfo(**tx)
        else:
            return TransactionInfo()

    def gettxoutaddress(self, address, mempool=True, type=0):
        """
        Returns details about unspent transaction outputs (UTXO) of an address

        Arguments:

        - *address* -- Target address for UTXO.
        - *mempool* -- Add memory pool transactions.
        - *type* -- Choose txout by type, 0 for normal and others for license.
        """
        return self.proxy.gettxoutaddress(address, mempool, type)

    def createrawtransaction(self, inputs, outputs):
        """
        Creates a raw transaction spending given inputs
        (a list of dictionaries, each containing a transaction id and an output number),
        sending to given address(es).

        Returns hex-encoded raw transaction.

        Example usage:
        >>> conn.createrawtransaction(
                [{"txid": "a9d4599e15b53f3eb531608ddb31f48c695c3d0b3538a6bda871e8b34f2f430c",
                  "vout": 0}],
                [{"address": "mkZBYBiq6DNoQEKakpMJegyDbw2YiNQnHT",
                  "value": 50,
                  "color": 1}]
                )


        Arguments:

        - *inputs* -- A list of {"txid": txid, "vout": n} dictionaries.
        - *outputs* -- A dictionary mapping (public) addresses to the amount
                       they are to be paid.
        """
        return self.proxy.createrawtransaction(inputs, outputs)

    def createmultisig(self, m, pubkeys):
        return self.proxy.createmultisig(m, pubkeys)

    def addmultisigaddress(self, m, pubkeys):
        return self.proxy.addmultisigaddress(m, pubkeys)

    def signrawtransaction(self, hexstring, previous_transactions=None, private_keys=None):
        """
        Sign inputs for raw transaction (serialized, hex-encoded).

        Returns a dictionary with the keys:
            "hex": raw transaction with signature(s) (hex-encoded string)
            "complete": 1 if transaction has a complete set of signature(s), 0 if not

        Arguments:

        - *hexstring* -- A hex string of the transaction to sign.
        - *previous_transactions* -- A (possibly empty) list of dictionaries of the form:
            {"txid": txid, "vout": n, "scriptPubKey": hex, "redeemScript": hex}, representing
            previous transaction outputs that this transaction depends on but may not yet be
            in the block chain.
        - *private_keys* -- A (possibly empty) list of base58-encoded private
            keys that, if given, will be the only keys used to sign the transaction.
        """
        return dict(self.proxy.signrawtransaction(hexstring, previous_transactions, private_keys))

    def decoderawtransaction(self, hexstring):
        """
        Produces a human-readable JSON object for a raw transaction.

        Arguments:

        - *hexstring* -- A hex string of the transaction to be decoded.
        """
        return dict(self.proxy.decoderawtransaction(hexstring))

    def sendrawtransaction(self, hexstring):
        return self.proxy.sendrawtransaction(hexstring)

    def listsinceblock(self, block_hash):
        res = self.proxy.listsinceblock(block_hash)
        res['transactions'] = [TransactionInfo(**x) for x in res['transactions']]
        return res

    def listaddressgroupings(self):
        '''
        Lists groups of addresses which have had their common ownership made public
        by common use as inputs or as the resulting change in past transactions.
        '''
        return self.proxy.listaddressgroupings()

    def listreceivedbyaddress(self, minconf=1, includeempty=False):
        """
        Returns a list of addresses.

        Each address is represented with a :class:`~gcoinrpc.data.AddressInfo` object.

        Arguments:

        - *minconf* -- Minimum number of confirmations before payments are included.
        - *includeempty* -- Whether to include addresses that haven't received any payments.

        """
        return [AddressInfo(**x) for x in
                self.proxy.listreceivedbyaddress(minconf, includeempty)]

    def listaccounts(self, minconf=1, as_dict=False):
        """
        Returns a list of account names.

        Arguments:

        - *minconf* -- Minimum number of confirmations before payments are included.
        - *as_dict* -- Returns a dictionary of account names, with their balance as values.
        """
        if as_dict:
            return dict(self.proxy.listaccounts(minconf))
        else:
            return self.proxy.listaccounts(minconf).keys()

    def listreceivedbyaccount(self, minconf=1, includeempty=False):
        """
        Returns a list of accounts.

        Each account is represented with a :class:`~gcoinrpc.data.AccountInfo` object.

        Arguments:

        - *minconf* -- Minimum number of confirmations before payments are included.

        - *includeempty* -- Whether to include addresses that haven't received any payments.
        """
        return [AccountInfo(**x) for x in
                self.proxy.listreceivedbyaccount(minconf, includeempty)]

    def listtransactions(self, account=None, count=10, from_=0, address=None):
        """
        Returns a list of the last transactions for an account.

        Each transaction is represented with a :class:`~gcoinrpc.data.TransactionInfo` object.

        Arguments:

        - *account* -- Account to list transactions from. Return transactions from
                       all accounts if None.
        - *count* -- Number of transactions to return.
        - *from_* -- Skip the first <from_> transactions.
        - *address* -- Receive address to consider
        """
        accounts = [account] if account is not None else self.listaccounts(as_dict=True).keys()
        return [TransactionInfo(**tx) for acc in accounts for
                tx in self.proxy.listtransactions(acc, count, from_) if
                address is None or tx["address"] == address]

    def listwalletaddress(self, first_n_items=None):
        """
        list all addresses in the wallet

        Arguments:

        - *first_n_items* -- List first n wallet addresses
        """
        if first_n_items is None:
            return self.proxy.listwalletaddress()
        else:
            return self.proxy.listwalletaddress(first_n_items)

    def listonewalletaddress(self, rank=0):
        """
        list {rank}th address in the wallet

        Arguments:

        - *rank* -- List {rank}th wallet address
        """
        return self.proxy.listonewalletaddress(rank)

    def backupwallet(self, destination):
        """
        Safely copies ``wallet.dat`` to *destination*, which can be a directory or a path
        with filename.

        Arguments:
        - *destination* -- directory or path with filename to backup wallet to.

        """
        return self.proxy.backupwallet(destination)

    def validateaddress(self, validateaddress):
        """
        Validate a bitcoin address and return information for it.

        The information is represented by a :class:`~gcoinrpc.data.AddressValidation` object.

        Arguments: -- Address to validate.


        - *validateaddress*
        """
        return AddressValidation(**self.proxy.validateaddress(validateaddress))

    def getbalance(self, account=None, minconf=None):
        """
        Get the current balance, either for an account or the total server balance.

        Arguments:
        - *account* -- If this parameter is specified, returns the balance in the account.
        - *minconf* -- Minimum number of confirmations required for transferred balance.

        """
        args = []
        if account is not None:
            args.append(account)
            if minconf is not None:
                args.append(minconf)
        return self.proxy.getbalance(*args)

    def getaddressbalance(self, bitcoinaddress, minconf=None):
        """
        Get the current balance of specified bitcoin address.

        Arguments:
        - *bitcoinaddress* -- If this parameter is specified, returns the balance of specified address.
        - *minconf* -- Minimum number of confirmations required for transferred balance.

        """
        args = []

        args.append(bitcoinaddress)
        if minconf is not None:
            args.append(minconf)
        return self.proxy.getaddressbalance(*args)

    def move(self, fromaccount, toaccount, amount, minconf=1, comment=None):
        """
        Move from one account in your wallet to another.

        Arguments:

        - *fromaccount* -- Source account name.
        - *toaccount* -- Destination account name.
        - *amount* -- Amount to transfer.
        - *minconf* -- Minimum number of confirmations required for transferred balance.
        - *comment* -- Comment to add to transaction log.

        """
        if comment is None:
            return self.proxy.move(fromaccount, toaccount, amount, minconf)
        else:
            return self.proxy.move(fromaccount, toaccount, amount, minconf, comment)

    def sendfrom(self, frombitcoinaddress, tobitcoinaddress, amount, minconf=1, comment=None,
                 comment_to=None):
        """
        Sends amount from a bitcoinaddress to another bitcoinaddress. This method will fail
        if there is less than amount bitcoins with minconf confirmations in the account's
        balance (unless account is the empty-string-named default account; it
        behaves like the sendtoaddress method). Returns transaction ID on success.

        Arguments:

        - *frombitcoinaddress* -- Bitcoin address to send from.
        - *tobitcoinaddress* -- Bitcoin address to send to.
        - *amount* -- Amount to send (float, rounded to the nearest 0.01).
        - *minconf* -- Minimum number of confirmations required for transferred balance.
        - *comment* -- Comment for transaction.
        - *comment_to* -- Comment for to-address.

        """
        if comment is None:
            return self.proxy.sendfrom(frombitcoinaddress, tobitcoinaddress, amount, minconf)
        elif comment_to is None:
            return self.proxy.sendfrom(frombitcoinaddress, tobitcoinaddress, amount, minconf, comment)
        else:
            return self.proxy.sendfrom(frombitcoinaddress, tobitcoinaddress, amount, minconf,
                                       comment, comment_to)

    def sendmany(self, fromaccount, todict, minconf=1, comment=None):
        """
        Sends specified amounts from account's balance to bitcoinaddresses. This method will fail
        if there is less than total amount bitcoins with minconf confirmations in the account's
        balance (unless account is the empty-string-named default account; Returns transaction ID
        on success.

        Arguments:

        - *fromaccount* -- Account to send from.
        - *todict* -- Dictionary with Bitcoin addresses as keys and amounts as values.
        - *minconf* -- Minimum number of confirmations required for transferred balance.
        - *comment* -- Comment for transaction.

        """
        if comment is None:
            return self.proxy.sendmany(fromaccount, todict, minconf)
        else:
            return self.proxy.sendmany(fromaccount, todict, minconf, comment)

    def verifymessage(self, bitcoinaddress, signature, message):
        """
        Verifies a signature given the bitcoinaddress used to sign,
        the signature itself, and the message that was signed.
        Returns :const:`True` if the signature is valid, and :const:`False` if it is invalid.

        Arguments:

        - *bitcoinaddress* -- the bitcoinaddress used to sign the message
        - *signature* -- the signature to be verified
        - *message* -- the message that was originally signed

        """
        return self.proxy.verifymessage(bitcoinaddress, signature, message)

    def getwork(self, data=None):
        """
        Get work for remote mining, or submit result.
        If data is specified, the server tries to solve the block
        using the provided data and returns :const:`True` if it was successful.
        If not, the function returns formatted hash data (:class:`~gcoinrpc.data.WorkItem`)
        to work on.

        Arguments:

        - *data* -- Result from remote mining.

        """
        if data is None:
            # Only if no data provided, it returns a WorkItem
            return WorkItem(**self.proxy.getwork())
        else:
            return self.proxy.getwork(data)

    def listunspent(self, addresses, color=None, minconf=1, maxconf=999999):
        """
        Returns a list of unspent transaction inputs in the wallet.

        Arguments:

        - *color* -- If specified, looks for UTXOs with this color.

        - *minconf* -- Minimum number of confirmations required to be listed.

        - *maxconf* -- Maximal number of confirmations allowed to be listed.


        """
        if color is None:
            return [TransactionInfo(**tx).__dict__ for tx in
                    self.proxy.listunspent(minconf, maxconf, addresses)]
        else:
            return [TransactionInfo(**tx).__dict__ for tx in
                    self.proxy.listunspent(minconf, maxconf, addresses, color)]


    def keypoolrefill(self, kpSize=None):
        """
        Fills the keypool, requires wallet passphrase to be set.

        Arguments:

        - *kpSize* -- refill keypool with kpSize or with default size given by bitocind Options: -keypool.
        """
        if kpSize is None:
            return self.proxy.keypoolrefill()
        else:
            return self.proxy.keypoolrefill(kpSize)

    def walletpassphrase(self, passphrase, timeout, dont_raise=False):
        """
        Stores the wallet decryption key in memory for <timeout> seconds.

        - *passphrase* -- The wallet passphrase.

        - *timeout* -- Time in seconds to keep the wallet unlocked
                       (by keeping the passphrase in memory).

        - *dont_raise* -- instead of raising `~gcoinrpc.exceptions.WalletPassphraseIncorrect`
                          return False.
        """
        try:
            self.proxy.walletpassphrase(passphrase, timeout)
            return True
        except BitcoinException as exception:
            if dont_raise:
                if isinstance(exception, WalletPassphraseIncorrect):
                    return False
                elif isinstance(exception, WalletAlreadyUnlocked):
                    return True
            raise exception

    def walletlock(self):
        """
        Removes the wallet encryption key from memory, locking the wallet.
        After calling this method, you will need to call walletpassphrase
        again before being able to call any methods which require the wallet
        to be unlocked.
        """
        return self.proxy.walletlock()

    def walletpassphrasechange(self, oldpassphrase, newpassphrase, dont_raise=False):
        """
        Changes the wallet passphrase from <oldpassphrase> to <newpassphrase>.

        Arguments:

        - *dont_raise* -- instead of raising `~gcoinrpc.exceptions.WalletPassphraseIncorrect`
                          return False.
        """
        try:
            self.proxy.walletpassphrasechange(oldpassphrase, newpassphrase)
            return True
        except BitcoinException as exception:
            if dont_raise and isinstance(exception, WalletPassphraseIncorrect):
                return False
            raise exception

    def dumpprivkey(self, address):
        """
        Returns the private key belonging to <address>.

        Arguments:

        - *address* -- Bitcoin address whose private key should be returned.
        """
        return self.proxy.dumpprivkey(address)

    def signmessage(self, address, message):
        """
        Sign messages, returns the signature

        :param address: Bitcoin address used to sign a message
        :type address: str or unicode
        :param message: The message to sign
        :type message: str or unicode
        :rtype: unicode
        """
        return self.proxy.signmessage(address, message)

    def verifymessage(self, address, signature, message):
        """
        Verify a signed message

        :param address: Bitcoin address used to sign a message
        :type address: str or unicode
        :param signature: The signature
        :type signature: unicode
        :param message: The message to sign
        :type message: str or unicode
        :rtype: bool
        """
        return self.proxy.verifymessage(address, signature, message)

    def encodelicenseinfo(self, licenseinfo):
        """
        Create a license info string from json format.

        Returns hex-encoded license information.

        Example usage:
        >>> conn.encodelicenseinfo(
                {"version": 1,
                 "name": "alice",
                 "description": "some one",
                 "issuer": "issuer",
                 "divisibility": True,
                 "fee_type": "fixed",
                 "fee_rate": 0.0,
                 "fee_collector": "collectaddr",
                 "mint_schedule": "free",
                 "member_control": True,
                 "metadata_link": "hyperlink",
                 "metadata_hash": "hash"})

        Arguments:

        - *licenseinfo* -- A dictionaries.
        """
        licenseinfo_bytes = dict()
        for key in licenseinfo.keys():
            if type(licenseinfo[key]) == unicode:
                licenseinfo_bytes[key] = licenseinfo[key].encode('utf-8')
            else:
                licenseinfo_bytes[key] = licenseinfo[key]
        return self.proxy.encodelicenseinfo(licenseinfo_bytes)

    def decodelicenseinfo(self, hexstring):
        """
        Returns a JSON object representing the serialized licenseinfo.
        """
        return self.proxy.decodelicenseinfo(hexstring)

    def sendlicensetoaddress(self, address, color, hexstring=None):
        """
        Send the license to <address>

        Arguments:

        - *address* -- address which have right to issue color_id
        - *color* -- color id
        - *licenseinfo* -- hex-encoded license info string of this color
        """
        if hexstring is None:
            return self.proxy.sendlicensetoaddress(address, color)
        else:
            return self.proxy.sendlicensetoaddress(address, color, hexstring)

    def getmemberlist(self):
        """
        Get aliances information
        """
        return self.proxy.getmemberlist()

    def getmempoolinfo(self):
        """
        Get information about the nodes current transaction memory pool
        """
        return self.proxy.getmempoolinfo()

    def getlicenselist(self):
        """
        Get licenses information
        """
        return self.proxy.getlicenselist()

    def getlicenseinfo(self, color_id):
        """
        Get licenseinfo of color
        """
        result = self.proxy.getlicenseinfo(color_id)
        for key in result.keys():
            if type(result[key]) == unicode:
                result[key] = result[key].encode('latin-1').decode('utf-8')
        return result

    def mint(self, amount, color_id):
        """
        Mint money if this wallet has license

        Arguments:

        - *amount* -- amount which wants to be minted

        - *color_id* -- color id which wants to be minted
        """
        return self.proxy.mint(amount, color_id)

    def importaddress(self, bitcoinaddress, account='', rescan=True):
        """
        Adds an address to the wallet without the associated private key.

        Allowing you to watch for transactions affecting that address
        without being able to spend any of its outputs.

        Arguments:

        - *bitcoinaddress* -- an bitcoin address
        - *account* -- the account into which to place the address
        - *rescan* -- whether to rescan the block chain
        """
        return self.proxy.importaddress(bitcoinaddress, account, rescan)

    def importprivkey(self, private_key, account='', rescan=True, keypool=False):
        """
        Adds a private key to wallet.

        The key should be formatted in the wallet import format created by the `dumpprivkey` RPC.

        Arguments:

        - *private_key* -- an private key
        - *account* -- the account into which to place the address
        - *rescan* -- whether to rescan the block chain
        - *keypool* -- whether to import private_key to keypool
        """
        return self.proxy.importprivkey(private_key, account, rescan, keypool)

    def getkeypoolsize(self):
        """
        Returns the amount of remaining keys in keypool
        """
        return self.proxy.getkeypoolsize()

    def sendfromfeeaddress(self, frombitcoinaddress, tobitcoinaddress, feebitcoinaddress,
                           amount, color):
        """
        Sends some amount of the given color from a bitcoinaddress to another bitcoinaddress.
        The transaction fee will be subtracted from the feebitcoinaddress. Returns transaction
        ID on success.

        Arguments:

        - *frombitcoinaddress* -- Bitcoin address to send from.
        - *tobitcoinaddress* -- Bitcoin address to send to.
        - *feebitcoinaddress* -- Bitcoin address that will pay the fees of this transaction.
        - *amount* -- Amount to send (float, rounded to the nearest 0.01).
        - *color* -- Color id.
        """
        return self.proxy.sendfromfeeaddress(frombitcoinaddress, tobitcoinaddress, feebitcoinaddress,
                                             amount, color)
