from TradingView import SymbolSearch

#sym_search = SymbolSearch()
#results = sym_search.search("","BIST","TR")
results = SymbolSearch().search("","BIST","TR")
#for result in results[:30]:  # Show first 3 results
print(len(results))
for result in results:
	print(f"  - {result['symbol']}: {result['description']} ({result['exchange']})")

#results = sym_search.search("PATEK","BIST","TR")
results = SymbolSearch().search("PATEK","BIST","TR")
#for result in results[:30]:  # Show first 3 results
print(f"  - {results[0]['symbol']}: {results[0]['description']} ({results[0]['exchange']})")