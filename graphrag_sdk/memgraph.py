import mgclient

class MemQueryResult:
    def __init__(self):
        pass

class Memgraph:
    
    def __init__(self, host: str, port: int, username: str, password: str):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password

        self.connection = self.connect()

    def connect(self):
        try:
            connection = mgclient.connect(
                host = self.__host, port=self.__port, username=self.__username, password=self.__password
            )
            return connection
        except Exception as e:
            raise

    def query(self, query: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            results =  cursor.fetchall()
            # return [self._format_mgclient_result(row) for row in results]
            return results
        except Exception as e:
            raise
    
    def _format_mgclient_result(self, response):
        formatted = []
        for item in response:
            if isinstance(item, mgclient.Relationship):
                formatted.append({
                    "Relation_type": item.type,
                    "start_id": item.start_id,
                    "end_id": item.end_id,
                    "properties": item.properties
                })
            elif isinstance(item, mgclient.Node):
                formatted.append({
                    "id": item.id,
                    "Node_labels": list(item.labels),
                    "properties": item.properties
                })
            else:
                formatted.append(str(item))
        return formatted

    