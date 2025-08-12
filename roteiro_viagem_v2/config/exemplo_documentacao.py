#!/usr/bin/env python3
"""
Demonstração da documentação estilo Google em ação.

Este arquivo mostra como a documentação estilo Google torna o código
mais legível e auto-explicativo.

Exemplo de uso:
    python3 exemplo_documentacao.py
    
    # Ou importar e explorar
    from exemplo_documentacao import ExemploClasse
    help(ExemploClasse)
    help(ExemploClasse.calcular_complexo)
"""
from typing import NoReturn


class ExemploClasse:
    """
    Classe de exemplo demonstrando documentação estilo Google.
    
    Esta classe implementa operações matemáticas básicas com
    documentação completa para facilitar o entendimento.
    
    Attributes:
        nome (str): Nome da instância da classe
        valores (List[float]): Lista de valores numéricos
        ativo (bool): Status ativo/inativo da instância
    
    Example:
        # Criar uma instância
        obj = ExemploClasse("Calculadora", [1.0, 2.0, 3.0])
        
        # Usar métodos
        resultado = obj.calcular_soma()
        print(f"Soma: {resultado}")
        
        # Verificar status
        if obj.esta_ativo():
            print("Calculadora ativa!")
    
    Note:
        Todos os métodos são thread-safe e podem ser chamados
        simultaneamente de diferentes threads.
    """

    def __init__(self, nome: str, valores: list[float], ativo: bool = True):
        """
        Inicializa uma nova instância da classe.
        
        Args:
            nome (str): Nome descritivo da instância
            valores (List[float]): Lista de valores numéricos para processar
            ativo (bool, optional): Status inicial. Padrão: True
        
        Example:
            obj = ExemploClasse("Minha Lista", [10, 20, 30])
            print(obj.nome)  # "Minha Lista"
        
        Raises:
            ValueError: Se a lista de valores estiver vazia
        """
        if not valores:
            raise ValueError("Lista de valores não pode estar vazia")

        self.nome = nome
        """Nome descritivo da instância."""

        self.valores = valores
        """Lista de valores numéricos para processamento."""

        self.ativo = ativo
        """Status ativo/inativo da instância."""

    def calcular_soma(self) -> float:
        """
        Calcula a soma de todos os valores na lista.
        
        Returns:
            float: Soma total dos valores
            
        Example:
            obj = ExemploClasse("Teste", [1, 2, 3])
            soma = obj.calcular_soma()  # 6.0
            
        Note:
            Retorna 0.0 se a lista estiver vazia (não deve acontecer
            devido à validação no __init__).
        """
        return sum(self.valores)

    def calcular_media(self) -> float | None:
        """
        Calcula a média aritmética dos valores.
        
        Returns:
            Optional[float]: Média dos valores ou None se não houver valores
            
        Example:
            obj = ExemploClasse("Teste", [10, 20, 30])
            media = obj.calcular_media()  # 20.0
            
        Note:
            Retorna None se não houver valores para calcular a média.
        """
        if not self.valores:
            return None
        return sum(self.valores) / len(self.valores)

    def calcular_complexo(self, operacao: str, multiplicador: int | float = 1.0) -> float:
        """
        Executa operações matemáticas complexas nos valores.
        
        Esta função permite diferentes tipos de operações matemáticas
        com um multiplicador opcional.
        
        Args:
            operacao (str): Tipo de operação ('soma', 'produto', 'maximo')
            multiplicador (Union[int, float], optional): Multiplicador para o resultado. Padrão: 1.0
        
        Returns:
            float: Resultado da operação multiplicado pelo multiplicador
            
        Raises:
            ValueError: Se a operação não for reconhecida
            
        Example:
            obj = ExemploClasse("Teste", [2, 3, 4])
            
            # Soma com multiplicador
            resultado = obj.calcular_complexo("soma", 2.0)  # (2+3+4) * 2 = 18.0
            
            # Produto
            resultado = obj.calcular_complexo("produto")  # 2*3*4 = 24.0
            
            # Máximo
            resultado = obj.calcular_complexo("maximo", 0.5)  # 4 * 0.5 = 2.0
        
        Note:
            Operações suportadas: 'soma', 'produto', 'maximo'
        """
        if operacao == "soma":
            resultado = sum(self.valores)
        elif operacao == "produto":
            resultado = 1
            for valor in self.valores:
                resultado *= valor
        elif operacao == "maximo":
            resultado = max(self.valores)
        else:
            raise ValueError(f"Operação '{operacao}' não suportada")

        return resultado * multiplicador

    def esta_ativo(self) -> bool:
        """
        Verifica se a instância está ativa.
        
        Returns:
            bool: True se ativo, False caso contrário
            
        Example:
            obj = ExemploClasse("Teste", [1, 2, 3], ativo=False)
            if obj.esta_ativo():
                print("Ativo!")
            else:
                print("Inativo!")  # Será impresso
        """
        return self.ativo

    def __str__(self) -> str:
        """
        Representação em string da instância.
        
        Returns:
            str: String formatada com nome e status
            
        Example:
            obj = ExemploClasse("Minha Classe", [1, 2, 3])
            print(obj)  # "ExemploClasse: Minha Classe (Ativo)"
        """
        status = "Ativo" if self.ativo else "Inativo"
        return f"ExemploClasse: {self.nome} ({status})"


def demonstrar_documentacao() -> None:
    """
    Demonstra como a documentação estilo Google funciona na prática.
    
    Esta função cria instâncias da classe e mostra como a documentação
    torna o código auto-explicativo.
    
    Returns:
        None: Apenas imprime exemplos
        
    Example:
        demonstrar_documentacao()
        
        # Ou importar e usar
        from exemplo_documentacao import demonstrar_documentacao
        demonstrar_documentacao()
    """
    print("🚀 **Demonstração da Documentação Estilo Google**\n")

    # Criar instância
    obj = ExemploClasse("Calculadora Avançada", [10, 20, 30, 40])

    print(f"📝 Instância criada: {obj}")
    print(f"🔢 Valores: {obj.valores}")
    print(f"📊 Soma: {obj.calcular_soma()}")
    print(f"📈 Média: {obj.calcular_media()}")
    print(f"✨ Soma x2: {obj.calcular_complexo('soma', 2)}")
    print(f"🎯 Produto: {obj.calcular_complexo('produto')}")
    print(f"🏆 Máximo x0.5: {obj.calcular_complexo('maximo', 0.5)}")

    print("\n💡 **Como usar a documentação:**")
    print("   help(ExemploClasse)           # Documentação da classe")
    print("   help(obj.calcular_complexo)   # Documentação do método")
    print("   obj.__doc__                   # Docstring da classe")
    print("   obj.calcular_soma.__doc__     # Docstring do método")


def run_demo() -> NoReturn:
    """Executa a demonstração e encerra o programa"""
    demonstrar_documentacao()
    exit(0)


if __name__ == "__main__":
    run_demo()
