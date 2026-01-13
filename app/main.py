from app.dominio.cliente import Cliente
from app.repositorios.cliente_repositorio import ClienteRepositorio

repo = ClienteRepositorio()
cliente = Cliente("João", "51999999999")
repo.inserir(cliente)

print(repo.listar())
