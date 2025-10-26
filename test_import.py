
try:
    import moviepy
    print("SUCESSO: A biblioteca 'moviepy' foi importada.")
except ImportError as e:
    print(f"FALHA: Não foi possível importar a biblioteca 'moviepy'. Erro: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
