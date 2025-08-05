from web3 import Web3

INFURA_URL = "https://mainnet.infura.io/v3/446fe3c4dc9249879ecc7d238670d2ea"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

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
]  # Use Uniswap V2 Router ABI

#exchange addresses
UNISWAP_ROUTER = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"  # Uniswap V2
SUSHI_ROUTER = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"    # SushiSwap

#token addresses
USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

#contracts
router_uni = w3.eth.contract(address=UNISWAP_ROUTER, abi=ROUTER_ABI)
router_sushi = w3.eth.contract(address=SUSHI_ROUTER, abi=ROUTER_ABI)

def get_exchange_price(router, token_in, token_out, amount):
    try:
        amount_out = router.functions.getAmountsOut(amount, [token_in, token_out]).call()
        return amount_out[1] / 10**18  # depends on token decimals
    except Exception as e:
        print(f"Error: {e}")
        return None
    
# def get_token_price(router, token){
#     try: 
#       price = router.functions.
# }
    
# 1 USDC = 1,000,000 (6 decimals)
amount_in = 1_000_000

price = get_exchange_price(router_uni, USDT, WETH, amount_in)
print(price)