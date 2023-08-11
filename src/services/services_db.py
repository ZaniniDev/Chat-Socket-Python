import sqlite3


class ServicoSQLite:
    def __init__(self, db_file):
        self.conn = None
        self.db_file = db_file

    def conectar(self):
        """Conecta ao banco de dados."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            # print("Conexão ao banco de dados estabelecida com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def desconectar(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            # print("Conexão ao banco de dados encerrada.")

    def executar_query(self, query, params=None):
        """Executa uma consulta SQL."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            
            # Obtém o ID da última linha inserida, caso seja uma inserção (INSERT)
            if query.strip().lower().startswith("insert"):
                last_row_id = cursor.lastrowid
                return last_row_id
            
            # Se não for uma inserção, retorna os dados retornados pela consulta (se houver)
            return cursor.fetchall()        
        except sqlite3.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return None

    def executar_insert(self, table, columns, values):
        """Executa uma inserção de dados na tabela."""
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(values))})"
        return self.executar_query(query, values)

    def executar_update(self, table, set_values, where_clause, where_params=None):
        """Executa uma atualização de dados na tabela."""
        set_clause = ", ".join([f"{column} = ?" for column in set_values])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = [*set_values.values()]
        if where_params:
            params.extend(where_params)
        return self.executar_query(query, params)

    def executar_delete(self, table, where_clause, where_params=None):
        """Executa uma exclusão de dados na tabela."""
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return self.executar_query(query, where_params)


# Exemplo de uso
if __name__ == "__main__":
    # Criando uma instância do serviço SQLite
    servico_db = ServicoSQLite("exemplo.db")

    # Conectando ao banco de dados
    servico_db.conectar()

    # Executando uma consulta SELECT
    resultado = servico_db.executar_query("SELECT * FROM tabela")
    print(resultado)

    # Executando uma inserção de dados
    servico_db.executar_insert("tabela", ["coluna1", "coluna2"], ["valor1", "valor2"])

    # Executando uma atualização de dados
    servico_db.executar_update("tabela", {"coluna1": "novo_valor"}, "coluna2 = ?", ["valor2"])

    # Executando uma exclusão de dados
    servico_db.executar_delete("tabela", "coluna1 = ?", ["valor1"])

    # Desconectando do banco de dados
    servico_db.desconectar()
