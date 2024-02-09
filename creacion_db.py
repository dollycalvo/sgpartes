import sqlite3

try:
    conn = sqlite3.connect("soportes.db")
    cursor = conn.cursor()

    sqls = []
    sqls.append("""
        CREATE TABLE IF NOT EXISTS agentes (
            id_agente INTEGER PRIMARY KEY,
            legajo INTEGER NOT NULL,
            apellidos TEXT NOT NULL,
            nombres TEXT NOT NULL,
            email_agente TEXT NOT NULL,
            jefe_directo TEXT NOT NULL,
            email_jefe_directo TEXT NOT NULL,
            password TEXT NOT NULL
        )    
    """)

    sqls.append("""
        CREATE TABLE IF NOT EXISTS planilla (
            id_planilla INTEGER PRIMARY KEY,
            id_agente INTEGER NOT NULL,
            mes TINYINT NOT NULL,
            año SMALLINT NOT NULL,
            presentado BOOLEAN NOT NULL DEFAULT FALSE,
            FOREIGN KEY(id_agente) REFERENCES agentes(id_agente)
        )    
    """)

    sqls.append("""
        CREATE TABLE IF NOT EXISTS registro_diario (
            id_registro_diario INTEGER PRIMARY KEY,
            id_planilla SMALLINT NOT NULL,
            dia TINYINT NOT NULL,
            codigo CHAR,
            observaciones TEXT,
            FOREIGN KEY(id_planilla) REFERENCES planilla(id_planilla)
        )    
    """)

    # for i in range(0, len(sqls)):
    #     cursor.execute(sqls[i])
        # print(sqls[i])
        
    # cursor.execute("INSERT INTO agentes (id_agente, legajo, apellidos, nombres, email_agente, jefe_directo, email_jefe_directo, password) VALUES (NULL, 1234562, \"Guimaraenz\", \"Carlos Roberto\", \"a\", \"b\", \"c\", \"pw\")")
    # cursor.execute("INSERT INTO agentes (id_agente, legajo, apellidos, nombres, email_agente, jefe_directo, email_jefe_directo, password) VALUES (NULL, 1234562, \"Olmos\", \"Carlos Roberto\", \"a\", \"b\", \"c\", \"pw\")")
    # conn.commit()

    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    cursor.close()
    
    print("El archivo de base de datos soportes.db ha sido creado")

except sqlite3.Error as error:
    print("Han existido errores en la conexión a la base de datos", error)
finally:
    if conn:
        conn.close()
        print("The Sqlite connection is closed")
