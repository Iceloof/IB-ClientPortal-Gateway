import requests
import urllib3
import time
urllib3.disable_warnings(
	urllib3.exceptions.InsecureRequestWarning
)
"""
SQQQ: 537765515
TQQQ: 72539702
"""
class API:
	def __init__(self, url="https://localhost:5000", ssl=False) -> None:
		self.url = f"{url}/v1/api/"
		self.ssl = ssl
		self.version = '1.0.1'
		# self.validated = self.get_validate()
		# while self.validated == "Authentication failed" or self.validated == "System failed":
		# 	print('Waiting for authentication')
		# 	time.sleep(5)
		# 	self.validated = self.get_validate()
	
	def getVersion(self):
		return self.version

	def get_validate(self) -> list:
		response = requests.get(f"{self.url}sso/validate", verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		elif response.status_code == 401:
			return "Authentication failed"
		else:
			return "System failed"
		
	def ping_server(self) -> dict:
		response = requests.post(f"{self.url}tickle", verify=self.ssl)
		if response.status_code == 200:
			return True
		else:
			return False

	def get_status(self) -> dict:
		response = requests.post(f"{self.url}iserver/auth/status", verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
 
	def reauthenticate(self) -> None:
		response = requests.post(f"{self.url}iserver/reauthenticate", verify=self.ssl)
		print("Reauthenticating ...")
		if response.status_code == 200:
			return response.json()
		else:
			return None
 
	def logout(self) -> None:
		response = requests.post(f"{self.url}logout", verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
 
	def get_future_conids(self, symbol: str) -> list:
		query = {"symbols": symbol}
		response = requests.get(f"{self.url}trsrv/futures", params=query, verify=self.ssl)
		if response.status_code == 200:
			try:
				return response.json()[symbol][0]['conid']
			except:
				return None
		else:
			return None

	def get_stock_conids(self, symbol: str, contract_filters: dict = {"isUS": True}) -> list:
		query = {"symbols": symbol}
		response = requests.get(f"{self.url}trsrv/stocks", params=query, verify=self.ssl)
		if response.status_code == 200:
			try:
				dic = response.json()
				def filter_instrument(instrument: dict) -> bool:
					def apply_filters(x: dict, filters: dict) -> list:
						positives = list(
								filter(
										lambda x: x,
										[x.get(key) == val for key, val in filters.items()],
								)
						)
						return len(positives) == len(filters)
    
					if contract_filters:
							instrument["contracts"] = list(
									filter(
											lambda x: apply_filters(x, contract_filters),
											instrument["contracts"],
									)
							)

					return len(instrument["contracts"]) > 0

				dic[symbol] = list(filter(filter_instrument, dic[symbol]))
				return dic[symbol][0]["contracts"][0]["conid"]
			except:
				return None
		else:
			return None
 
	def find_conids(self, conids: list) -> list:
		query = {"conids": conids}
		response = requests.get(f"{self.url}trsrv/secdef", params=query, verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None

	def get_history(
        self,
        conid: int,
        period="1w",
        bar="1d",
        outsideRth=False,
    ) -> dict:
		query = {
            "conid": conid,
            "period": period,
            "bar": bar,
            "outsideRth": outsideRth,
        }
		response = requests.get(f"{self.url}iserver/marketdata/history", params=query, verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
 
	def get_history_beta(
        self,
        conid: int,
        period="1w",
        bar="1d",
        outsideRth=False,
    ) -> dict:
		query = {
            "conid": conid,
            "period": period,
            "bar": bar,
            "outsideRth": outsideRth,
        }
		response = requests.get(f"{self.url}hmds/history", params=query, verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
 
	def get_snapshot(
        self,
        conids: str,
        since: int,
        fields: str,
    ) -> dict:
		query = {
            "conids": conids,
            "since": since,
            "fields": fields,
        }
		response = requests.get(f"{self.url}iserver/marketdata/snapshot", params=query, verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None

	def get_snapshot_beta(
        self,
        conids: str,
        fields: str,
    ) -> dict:
		query = {
            "conids": conids,
            "fields": fields,
        }
		response = requests.get(f"{self.url}md/snapshot", params=query, verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None

	def get_accounts(self) -> list:
		response = requests.get(f"{self.url}portfolio/accounts", verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
 
	def get_account_meta(self, accountId: str) -> list:
		response = requests.get(f"{self.url}portfolio/{accountId}/meta", verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
 
	def get_account_summary(self, accountId: str) -> list:
		response = requests.get(f"{self.url}portfolio/{accountId}/summary", verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
 
	def get_account_PDT(self, accountId: str) -> list:
		response = requests.get(f"{self.url}portfolio/{accountId}/summary", verify=self.ssl)
		if response.status_code == 200:
			try:
				return response.json()['daytradesremaining']['value']
			except:
				return None
		else:
			return None
 
	def get_account_ledger(self, accountId: str) -> list:
		response = requests.get(f"{self.url}portfolio/{accountId}/ledger", verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
 
	def get_trades(self) -> list:
		response = requests.get(f"{self.url}iserver/account/trades", verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
	
	"""
	filters: cancelled, filled, submitted
	"""
	def get_orders(self, filters: list = []) -> list:
		query = {
            "filters": filters,
        }
		response = requests.get(f"{self.url}iserver/account/orders", params=query, verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None

	def get_orders(self, orderId: str) -> list:
		response = requests.get(f"{self.url}iserver/account/order/status/{orderId}", params=query, verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None

	def reply_yes(self, id: str) -> dict:
		answer = {"confirmed": True}
		response = requests.post(f"{self.url}iserver/reply/{id}", json=answer, verify=self.ssl)
		if response.status_code == 200:
			try:
				return response.json()[0]
			except:
				return None
		else:
			return None

	def _reply_all_yes(self, response, reply_yes_to_all: bool) -> dict:
		dic = response.json()[0]
		if reply_yes_to_all:
			while "order_id" not in dic.keys():
				print("Answering yes to ...")
				print(dic["message"])
				dic = self.reply_yes(dic["id"])
		return dic

	def submit_orders(self, accountId: str, list_of_orders: list, reply_yes=True) -> dict:	
		response = requests.post(
				f"{self.url}iserver/account/{accountId}/orders",
				json={"orders": list_of_orders},
				verify=self.ssl,
		)
		if response.status_code == 200:
			try:
				return self._reply_all_yes(response, reply_yes)
			except:
				return None
		else:
			return None

	def create_order(self, accountId: str, conid: int, price: float, quantity: int, side: str, orderType: str='LMT', outsideRTH: bool=True, tif: str='GTC', useAdaptive: bool=True, isCcyConv: bool=False):
		order = [{"acctId": accountId, "conid": conid, "price": price, "quantity": quantity, "side": side, "orderType": orderType, "outsideRTH": outsideRTH, "tif": tif, "useAdaptive": useAdaptive, "isCcyConv": isCcyConv}]
		return self.submit_orders(accountId, order)
 
	def cancel_order(self, accountId: str, orderId: str) -> dict:
		response = requests.delete(f"{self.url}iserver/account/{accountId}/order/{orderId}", verify=self.ssl)
		if response.status_code == 200:
			return response.json()
		else:
			return None
