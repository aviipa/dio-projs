import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

# ====================================================================
# CONSTANTES
# ====================================================================
AGENCIA_DEFAULT = "0001"
LIMITE_SAQUE_DEFAULT = 500
LIMITE_SAQUES_DEFAULT = 3

# ====================================================================
# PARTE 1: INTERFACES E CLASSES ABSTRATAS
# ====================================================================

class Transacao(ABC):
    """
    Interface (Classe Abstrata) que define o contrato para transações.
    O decorador @abstractmethod obriga as subclasses a implementarem este método.
    """
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    @abstractmethod
    def registrar(self, conta: 'Conta') -> None:
        pass


# ====================================================================
# PARTE 2: CLASSES DE DOMÍNIO (BANCO)
# ====================================================================

class Historico:
    """Responsável por armazenar as transações de uma conta."""
    def __init__(self) -> None:
        self._transacoes: List[dict] = []

    @property
    def transacoes(self) -> List[dict]:
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao) -> None:
        # Armazena um dicionário com os dados da transação e a data atual
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Conta:
    """Classe base que representa uma conta genérica."""
    def __init__(self, numero: int, cliente: 'Cliente') -> None:
        self._saldo = 0.0
        self._numero = numero
        self._agencia = AGENCIA_DEFAULT
        self._cliente = cliente
        self._historico = Historico() # Composição: Conta TEM UM Histórico

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int) -> 'Conta':
        # Método de fábrica para criar uma instância de Conta
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> 'Cliente':
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
        saldo = self.saldo
        
        if valor > saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        
        if valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False


class ContaCorrente(Conta):
    """Subclasse de Conta com regras específicas de limite e quantidade de saques."""
    def __init__(self, numero: int, cliente: 'Cliente', 
                 limite: float = LIMITE_SAQUE_DEFAULT, 
                 limite_saques: int = LIMITE_SAQUES_DEFAULT) -> None:
        super().__init__(numero, cliente) # Chama o construtor da classe pai
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        # Conta a quantidade de saques já realizados no histórico
        numero_saques = len(
            [t for t in self.historico.transacoes if t["tipo"] == "Saque"]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        if excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        # Se passou pelas validações específicas, chama o sacar da classe pai (Conta)
        return super().sacar(valor)

    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


# ====================================================================
# PARTE 3: CLASSES DE TRANSAÇÃO CONCRETAS
# ====================================================================

class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> None:
        # A transação tenta efetivar o saque na conta
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> None:
        # A transação tenta efetivar o depósito na conta
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# ====================================================================
# PARTE 4: CLIENTES
# ====================================================================

class Cliente:
    def __init__(self, endereco: str) -> None:
        self.endereco = endereco
        self.contas: List[Conta] = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
        # O cliente inicia a transação, passando a conta alvo e a transação
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta) -> None:
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str) -> None:
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


# ====================================================================
# PARTE 5: FUNÇÕES AUXILIARES
# ====================================================================

def validar_cpf(cpf: str) -> bool:
    """Valida se o CPF contém exatamente 11 dígitos numéricos."""
    return len(cpf) == 11 and cpf.isdigit()


def obter_valor_float(mensagem: str) -> Optional[float]:
    """Obtém um valor float do usuário com tratamento de exceções."""
    while True:
        try:
            valor = float(input(mensagem))
            if valor > 0:
                return valor
            print("\n@@@ O valor deve ser positivo! @@@")
        except ValueError:
            print("\n@@@ Valor inválido! Digite um número. @@@")


# ====================================================================
# PARTE 6: MENU E LÓGICA DE INTERFACE (ADAPTADO)
# ====================================================================

def menu() -> str:
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


def filtrar_cliente(cpf: str, clientes: List[PessoaFisica]) -> Optional[PessoaFisica]:
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente: Cliente) -> Optional[Conta]:
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    # FIXO: Retorna a primeira conta para simplificar o desafio
    return cliente.contas[0]


def depositar(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = obter_valor_float("Informe o valor do depósito: ")
    if valor is None:
        return

    # Aqui ocorre o polimorfismo e a interação entre classes:
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = obter_valor_float("Informe o valor do saque: ")
    if valor is None:
        return

    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF (somente número): ")
    
    # Validação do formato do CPF
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! Deve conter exatamente 11 dígitos numéricos. @@@")
        return
    
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta: int, clientes: List[PessoaFisica], contas: List[Conta]) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    # Cria uma instância de ContaCorrente
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    
    # Adiciona a conta às listas necessárias
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas: List[Conta]) -> None:
    for conta in contas:
        print("=" * 100)
        # O print chama automaticamente o método __str__ da classe ContaCorrente
        print(textwrap.dedent(str(conta)))


def main() -> None:
    clientes: List[PessoaFisica] = []
    contas: List[Conta] = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


# Executa o programa
if __name__ == "__main__":
    main()