# IB Client Portal Gateway API

[![PyPI](https://img.shields.io/pypi/v/ib-cp-gateway)](https://pypi.org/project/ib-cp-gateway/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ib-cp-gateway)](https://pypistats.org/packages/ib-cp-gateway)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ib-cp-gateway)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/ib-cp-gateway)
![GitHub contributors](https://img.shields.io/github/contributors/Iceloof/IB-ClientPortal-Gateway)
![GitHub issues](https://img.shields.io/github/issues-raw/Iceloof/IB-ClientPortal-Gateway)
![GitHub Action](https://github.com/Iceloof/IB-ClientPortal-Gateway/workflows/GitHub%20Action/badge.svg)
![GitHub](https://img.shields.io/github/license/Iceloof/IB-ClientPortal-Gateway)

This is a simple IB Client Portal Gateway RESTFul api, IB Client Portal Gateway can be run on Raspberry Pi or any other ARM machine(IB Gateway and TWS are not able to run on ARM). If the api get error, it will return None rather than throw exception.
## Install
```
pip install ib-cp-gateway
```
or
```
pip install --upgrade ib-cp-gateway
```
## Usage
- Login/Authentication
You need go login through https://localhost:5000 before using this api. To run the IB Client Portal Gateway, you can use docker.
For ARM architecture,
```
docker run -d -it --restart=always --name cpgateway-docker -p 5000:5000 hurinhu/ib-clientportal-gateway:RPI4
```
For others,
```
docker run -d -it --restart=always --name cpgateway-docker -p 5000:5000 hurinhu/ib-clientportal-gateway
```
- Initializing
```
from IB import API
ib = API(url="https://localhost:5000", ssl=False)
```
- Check version
```
print(ib.getVersion())
```
- Check validate session
```
ib.get_validate()
```
- Ping server to keep alive
```
ib.ping_server()
```
- Get gateway status
```
ib.get_status()
```
- Re authentication
```
ib.reauthenticate()
```
- Logout
```
ib.logout()
```
- Get future conids
```
ib.get_future_conids(symbol)
```
- Get stock conids
```
ib.get_stock_conids(symbol,contract_filters={"isUS": True})
```
- Find conids details
```
ib.find_conids(conids)
```
- Get history data
```
ib.get_history(conid, period='1w',bar='id',outsideRth=False)
```
or
```
ib.get_history_beta(conid, period='1w',bar='id',outsideRth=False)
```
- Get snapshot data
```
ib.get_snapshot(conids,since,fields)
```
or
```
ib.get_snapshot_beta(conids,fields)
```
- Get account information
```
ib.get_accounts()
```
- Get account meta
```
ib.get_account_meta(accountId)
```
- Get account summary
```
ib.get_account_summary(accountId)
```
- Get account PDT
```
ib.get_account_PDT()
```
- Get account ledger (balance information)
```
ib.get_account_ledger(account)
```
- Get account trades
```
ib.get_trades()
```
- Get orders (filters: cancelled, filled, submitted)
```
ib.get_orders(filters=[])
```
or
```
ib.get_order_by_id(orderId)
```
- Create order (side: BUY, SELL)
```
ib.create_order(accountId, conid, price, quantity, side, orderType='LMT', outsideRTH=True, tif='GTC', useAdaptive=True, isCcyConv=False)
```
- Cancel order
```
ib.cancel_order(accountId, orderId)
```

Example
```
order = ib.create_order('UXXXXX', 72539702, 41.20, 200, 'BUY', 'LMT', True, 'GTC', True, False)
orderId = order['order_id']
ib.cancel_order('UXXXXX',orderId)
orders = ib.get_orders()
orders[0]['status'] # this is the last order status, it should be 'Cancelled' after cancel order
```
