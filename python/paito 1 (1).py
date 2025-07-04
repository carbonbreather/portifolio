import sqlite3
import os


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


conn = sqlite3.connect('astronomia.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS objetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    distancia REAL,
    id_categoria INTEGER,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id)
)
''')

conn.commit()


def cadastrar_categoria():
    nome = input('Nome da nova categoria (ex: Galáxia, Estrela): ')
    try:
        cursor.execute('INSERT INTO categorias (nome) VALUES (?)', (nome,))
        conn.commit()
        print('Categoria cadastrada com sucesso!')
    except Exception as e:
        print(f'Erro ao cadastrar categoria: {e}')

def listar_categorias():
    cursor.execute('SELECT id, nome FROM categorias')
    categorias = cursor.fetchall()
    print('\nCategorias disponíveis:')
    for cat in categorias:
        print(f'{cat[0]} - {cat[1]}')
    return categorias

def cadastrar_objeto():
    nome = input('Nome do objeto astronômico: ')
    tipo = input('Tipo (ex: planeta, estrela): ')
    distancia = float(input('Distância da Terra (em anos-luz): '))
    listar_categorias()
    id_categoria = int(input('ID da categoria do objeto: '))
    try:
        cursor.execute('''
            INSERT INTO objetos (nome, tipo, distancia, id_categoria)
            VALUES (?, ?, ?, ?)
        ''', (nome, tipo, distancia, id_categoria))
        conn.commit()
        print('Objeto cadastrado com sucesso!')
    except Exception as e:
        print(f'Erro ao cadastrar objeto: {e}')

def listar_objetos():
    cursor.execute('''
        SELECT o.id, o.nome, o.tipo, o.distancia, c.nome 
        FROM objetos o LEFT JOIN categorias c 
        ON o.id_categoria = c.id
    ''')
    objetos = cursor.fetchall()
    print('\nObjetos astronômicos:')
    for obj in objetos:
        print(f'{obj[0]} - {obj[1]} | Tipo: {obj[2]} | Distância: {obj[3]} AL | Categoria: {obj[4]}')

def excluir_objeto():
    listar_objetos()
    id_obj = int(input('Digite o ID do objeto a ser excluído: '))
    cursor.execute('DELETE FROM objetos WHERE id = ?', (id_obj,))
    conn.commit()
    print('Objeto excluído com sucesso!')

def alterar_objeto():
    listar_objetos()
    id_obj = int(input('Digite o ID do objeto a ser alterado: '))
    novo_nome = input('Novo nome: ')
    novo_tipo = input('Novo tipo: ')
    nova_dist = float(input('Nova distância (anos-luz): '))
    listar_categorias()
    nova_cat = int(input('Novo ID da categoria: '))
    cursor.execute('''
        UPDATE objetos 
        SET nome = ?, tipo = ?, distancia = ?, id_categoria = ?
        WHERE id = ?
    ''', (novo_nome, novo_tipo, nova_dist, nova_cat, id_obj))
    conn.commit()
    print('Objeto alterado com sucesso!')


def menu():
    while True:
        print('\n=== Biblioteca de Astronomia ===')
        print('1. Cadastrar categoria')
        print('2. Listar categorias')
        print('3. Cadastrar objeto astronômico')
        print('4. Listar objetos')
        print('5. Excluir objeto')
        print('6. Alterar objeto')
        print('0. Sair')
        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            cadastrar_categoria()
        elif opcao == '2':
            listar_categorias()
        elif opcao == '3':
            cadastrar_objeto()
        elif opcao == '4':
            listar_objetos()
        elif opcao == '5':
            excluir_objeto()
        elif opcao == '6':
            alterar_objeto()
        elif opcao == '0':
            break
        else:
            print('Opção inválida.')

    cursor.close()
    conn.close()

menu()
