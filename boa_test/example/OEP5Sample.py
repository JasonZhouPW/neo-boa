from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from boa.interop.Ontology.Native import Invoke
from boa.builtins import *

owner = ToScriptHash('Ad4pjz2bqep4RhQrUAzMuZJkBC3qJ1tZuT')

NAME = 'OEP5 Asset'
SYMBOL = 'Asset Symbol'

OWNER_BALANCE_PREFIX = 'Balance'
OWNER_OF_ASSET_PREFIX = 'OwnerOf'
APPROVE_PREFIX = 'Approve'
INITED = 'Initialized'
ASSET_INDEX_PREFIX = 'Index'
TOTAL_ASSET_COUNT = 'TotalCount'
ASSET_ID_PREFIX = 'AssetID'


ctx = GetContext()

selfAddr = GetExecutingScriptHash()

def Main(operation, args):
    if operation == 'init':
        return init()
    if operation == 'name':
        return name()
    if operation == 'symbol':
        return symbol()
    if operation == 'balanceOf':
        if len(args) != 1:
            return False
        owner = args[0]
        return balanceOf(owner)
    if operation == 'ownerOf':
        if len(args) != 1:
            return False
        assetID = args[0]
        return ownerOf(assetID)
    if operation == 'transfer':
        if len(args) != 2:
            return False
        toAcct = args[0]
        assetID = args[1]
        return transfer(toAcct, assetID)
    if operation == 'transferMulti':
        return transferMulti(args)
    if operation == 'approve':
        if len(args) != 2:
            return False
        toAcct = args[0]
        assetID = args[1]
        return approve(toAcct, assetID)
    if operation == 'takeOwnership':
        if len(args) != 2:
            return False
        toAcct = args[0]
        assetID = args[1]
        return takeOwnership(toAcct, assetID)
    if operation == 'tokenMetadata':
        if len(args) != 1:
            return False
        assetID = args[0]
        return tokenMetadata(assetID)
    if operation == 'buyAsset':
        if len(args) != 2:
            return False
        account = args[0]
        assetID = args[1]
        return buyAsset(account, assetID)
    if operation == 'queryAssetIDByIndex':
        if len(args) != 1:
            return False
        idx = args[0]
        return queryAssetIDByIndex(idx)
    if operation == 'queryAssetByID':
        if len(args) != 1:
            return False
        assetID = args[0]
        return queryAssetByID(assetID)
    if operation == 'queryAssetCount':
        return queryAssetCount()

    return False


def init():
    if not Get(ctx, INITED):
        Put(ctx, INITED, 'TRUE')

        a1 = {'Name': 'HEART A', 'Image': 'http://hearta.jpg'}
        a2 = {'Name': 'HEART 2', 'Image': 'http://heart2.jpg'}
        a3 = {'Name': 'HEART 3', 'Image': 'http://heart3.jpg'}
        a4 = {'Name': 'HEART 4', 'Image': 'http://heart4.jpg'}
        a5 = {'Name': 'HEART 5', 'Image': 'http://heart5.jpg'}
        a6 = {'Name': 'HEART 6', 'Image': 'http://heart6.jpg'}
        a7 = {'Name': 'HEART 7', 'Image': 'http://heart7.jpg'}
        a8 = {'Name': 'HEART 8', 'Image': 'http://heart8.jpg'}
        a9 = {'Name': 'HEART 9', 'Image': 'http://heart9.jpg'}
        a10 = {'Name': 'HEART 10', 'Image': 'http://heart10.jpg'}
        a11 = {'Name': 'HEART J', 'Image': 'http://heartj.jpg'}
        a12 = {'Name': 'HEART Q', 'Image': 'http://heartq.jpg'}
        a13 = {'Name': 'HEART K', 'Image': 'http://heartk.jpg'}


        cards = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13]

        for card in cards:
            createAsset(card['Name'], card['Image'], 'CARD')

        return True
    return False


def name():
    return NAME


def symbol():
    return SYMBOL


def balanceOf(owner):
    key = concatkey(OWNER_BALANCE_PREFIX, owner)
    return Get(ctx, key)


def ownerOf(assetID):
    key = concatkey(OWNER_OF_ASSET_PREFIX, assetID)
    return Get(ctx, key)


def transfer(toAcct, assetID):
    if checkToAcctAndAsset(toAcct, assetID) == False:
        return False

    key = concatkey(OWNER_OF_ASSET_PREFIX, assetID)
    oldowner = Get(ctx, key)
    Put(ctx, key, toAcct)
    increaseOwnerBalance(toAcct)
    Notify(['transfer', oldowner, toAcct, assetID])

    return True


def transferMulti(args):
    for p in args:
        if len(p) != 2:
            return False
        if transfer(p[0], p[1]) == False:
            raise Exception('Multi transfer failed!')
    return True


def approve(toAcct, assetID):
    if checkToAcctAndAsset(toAcct, assetID) == False:
        return False

    assetOwner = ownerOf(assetID)
    if not assetOwner:
        return False

    key = concatkey(concatkey(APPROVE_PREFIX, assetOwner), assetID)
    Put(ctx, key, toAcct)
    Notify(['approve', assetOwner, toAcct, assetID])
    return True


def takeOwnership(toAcct, assetID):
    if CheckWitness(toAcct) == False:
        return False

    assetOwner = ownerOf(assetID)
    if not assetOwner:
        return False

    key = concatkey(concatkey(APPROVE_PREFIX, assetOwner), assetID)
    approver = Get(ctx, key)
    if approver != toAcct:
        return False

    Delete(ctx, key)
    ownerKey = concatkey(OWNER_OF_ASSET_PREFIX, assetID)
    Put(ctx, ownerKey, assetID)
    increaseOwnerBalance(toAcct)
    Notify(['transfer',assetOwner, toAcct, assetID])

    return True


def concatkey(str1, str2):
    return concat(concat(str1, '_'), str2)


def checkToAcctAndAsset(toAcct, assetID):
    if len(toAcct) != 20:
        return False
    owner = ownerOf(assetID)
    if not owner:
        return False
    if CheckWitness(owner) == False:
        return False
    return True


def increaseOwnerBalance(acct):
    balance = balanceOf(acct)
    key = concatkey(OWNER_BALANCE_PREFIX, acct)
    Put(ctx, key, balance + 1)


def tokenMetadata(assetID):
    #for example
    return concatkey("tokenMetadata", assetID)


def createAsset(name, url, type):

    timestamp = GetTime()
    totalcount = Get(ctx,TOTAL_ASSET_COUNT)
    Put(ctx, TOTAL_ASSET_COUNT, totalcount+1)
    tmp = concatkey(concatkey(selfAddr, timestamp), totalcount + 1)
    assetID = hash256(tmp)

    asset = {'ID': assetID, 'Name': name, 'Image': url, 'Type': type}
    Put(ctx, concatkey(ASSET_INDEX_PREFIX, totalcount+1), assetID)
    Put(ctx, concatkey(ASSET_ID_PREFIX, assetID), Serialize(asset))


def buyAsset(account, assetID):
    if ownerOf(assetID):
        return False
    if CheckWitness(account) == False:
        return False
    if transferONT(account, selfAddr, 1):
        key = concatkey(OWNER_OF_ASSET_PREFIX, assetID)
        Put(ctx, key, account)
        increaseOwnerBalance(account)
        Notify(['transfer', '', account, assetID])
        return True
    return False


def queryAssetIDByIndex(idx):
    return Get(ctx, concatkey(ASSET_INDEX_PREFIX, idx))


def queryAssetByID(assetID):
    return Get(ctx, concatkey(ASSET_ID_PREFIX, assetID))


def queryAssetCount():
    return Get(ctx, TOTAL_ASSET_COUNT)


def transferONT(fromacct, toacct, amount):
    """
    transfer ONT
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    # ONT native contract address
    contractAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')

    if CheckWitness(fromacct):
        param = state(fromacct, toacct, amount)
        res = Invoke(1, contractAddress, 'transfer', [param])
        Notify(res)

        if res and res == b'\x01':
            return True
        else:
            return False

    else:
        return False
