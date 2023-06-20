from site_atividade import app

if __name__ == '__main__':

    """
    Ponto de entrada do programa.

    - Verifica se o módulo está sendo executado diretamente.
    - Se for o caso, inicia o servidor Flask para a execução da aplicação.
        - debug=True: Ativa o modo de depuração, exibindo mensagens de erro detalhadas em caso de falhas.
    """

    app.run(debug=True)


