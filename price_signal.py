from web3 import Web3

INFURA_URL = "https://mainnet.infura.io/v3/446fe3c4dc9249879ecc7d238670d2ea"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Use Uniswap V2 Router ABI
ROUTER_ABI =  [
    {
        "name": "getAmountsOut",
        "inputs": [
            {"name": "amountIn", "type": "uint256"},
            {"name": "path", "type": "address[]"}
        ],
        "outputs": [
            {"name": "", "type": "uint256[]"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]  

# Minimal ABI to get decimals
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
        "stateMutability": "view"
    }
]

#exchange addresses
UNISWAP_ROUTER = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"  # Uniswap V2
SUSHI_ROUTER = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"    # SushiSwap

#token addresses
token_addresses = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
    "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
    "UNI": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    "AAVE": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DdAE9",
    "MKR": "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2",
    "COMP": "0xc00e94Cb662C3520282E6f5717214004A7f26888",
    "CRV": "0xD533a949740bb3306d119CC777fa900bA034cd52",
    "XSGD": "0x70e8dE73cE538DA2bEEd35d14187F6959a8ecA96",
    "RNDR": "0x6De037ef9aD2725EB40118Bb1702EBb27e4Aeb24 ",
}


#contracts
router_uni = w3.eth.contract(address=UNISWAP_ROUTER, abi=ROUTER_ABI)
router_sushi = w3.eth.contract(address=SUSHI_ROUTER, abi=ROUTER_ABI)

def get_token_decimals(token_address):
    token_contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    try:
        return token_contract.functions.decimals().call()
    except Exception as e:
        print(f"Failed to fetch decimals for {token_address}: {e}")
        return None

def get_price(router, token_in, token_out, amount):
    try:
        amount_out = router.functions.getAmountsOut(amount, [token_in, token_out]).call()
        return amount_out[1] / amount  # depends on token decimals
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_price_difference(price_uni, price_sushi):
    difference = abs(price_uni - price_sushi) / min(price_uni, price_sushi)
    if (price_uni < price_sushi):
        return f"Buy on Uniswap, sell on Sushi. The difference is {difference}"
    if (price_sushi < price_uni):
        return f"Buy on Sushi, sell on Uniswap. The difference is {difference}"
    else:
        return "the price is equal"
    

for i in token_addresses.values():
    for j in token_addresses.values():
        if i == j:
            continue

        price_uni = get_price(router_uni, i, j, 1 * 10**get_token_decimals(i))
        price_sushi = get_price(router_sushi, i, j, 1 * 10**get_token_decimals(i))

        difference = get_price_difference(price_uni, price_sushi)
        print(f"compare {token_addresses.get()} with {j}")
        print(difference)






# price_uni = get_price(router_uni, WETH, USDT, 1 * 10**get_token_decimals(WETH))
# price_sushi = get_price(router_sushi, WETH, USDT, 1 * 10**get_token_decimals(WETH))

# difference = abs(price_uni - price_sushi) / min(price_uni, price_sushi)

# print("price_uni: " + str(price_uni))
# print("price_sushi: " + str(price_sushi))
# print("difference: " + str(difference))



# if difference > 0.01:
#     message = f"💸 Arbitrage Opportunity!\nUniswap: {price_uni}\nSushiSwap: {price_sushi}\nDiff: {round(difference*100, 2)}%"
#     send_telegram(message)

# import time

# while True:
#     check_prices()
#     time.sleep(10)  # or 60s, depending on how aggressive you want it


