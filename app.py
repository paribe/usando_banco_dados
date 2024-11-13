from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração básica
engine = create_engine('sqlite:///exemplo.db')  # Cria o banco de dados SQLite
Base = declarative_base()  # Cria a base para nossos modelos ORM

# Definindo o modelo de tabela (ORM)
class Usuario(Base):
    __tablename__ = 'usuarios'  # Nome da tabela

    id = Column(Integer, primary_key=True, autoincrement=True)  # Coluna ID
    nome = Column(String, nullable=False)  # Coluna Nome
    idade = Column(Integer, nullable=False)  # Coluna Idade

    def __repr__(self):
        return f"<Usuario(nome={self.nome}, idade={self.idade})>"

def main():
    # Criando a tabela no banco de dados
    Base.metadata.create_all(engine)

    # Criando uma sessão para interagir com o banco de dados
    Session = sessionmaker(bind=engine)
    session = Session()

    # Inserindo dados na tabela
    novo_usuario = Usuario(nome="Alice", idade=25)
    session.add(novo_usuario)  # Adiciona um usuário
    session.commit()  # Confirma a transação

    # Inserindo múltiplos usuários
    usuarios = [
        Usuario(nome="Bob", idade=30),
        Usuario(nome="Carlos", idade=35),
        Usuario(nome="Diana", idade=28),
    ]
    session.add_all(usuarios)
    session.commit()

    # Consultando dados
    print("Todos os usuários:")
    for usuario in session.query(Usuario).all():
        print(usuario)

    # Filtrando com cláusulas WHERE
    print("\nUsuários com idade maior que 28:")
    for usuario in session.query(Usuario).filter(Usuario.idade > 28):
        print(usuario)

    # Atualizando um registro
    usuario_para_atualizar = session.query(Usuario).filter_by(nome="Alice").first()
    if usuario_para_atualizar:
        usuario_para_atualizar.idade = 26
        session.commit()

    # Deletando um registro
    usuario_para_deletar = session.query(Usuario).filter_by(nome="Carlos").first()
    if usuario_para_deletar:
        session.delete(usuario_para_deletar)
        session.commit()

    # Verificando as atualizações finais
    print("\nDados após atualizações:")
    for usuario in session.query(Usuario).all():
        print(usuario)

    # Fechando a sessão
    session.close()

# Executa o código automaticamente se o script for executado diretamente
if __name__ == "__main__":
    main()
