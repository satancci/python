from hashlib import file_digest, sha256
from colorama import Back, init, Style, Fore
from pathlib import Path

def newprint(msg_erro, msg_solucao):
    print(f'''\n    {Back.RED}{Style.BRIGHT} ERRO {Style.RESET_ALL} {msg_erro}.
       {Fore.GREEN}➜ {msg_solucao}.{Fore.WHITE}\n''')
    
def fore_cyan(msg):
    return f"{Fore.CYAN}{msg}{Fore.WHITE}"

def add_space(texto, agrupamento = 4):
    return ' '.join([texto.upper()[i:i+agrupamento] for i in range(0, len(texto), agrupamento)]).upper()

def hash_arquivo(caminho, space = False):
    init()
    try:
        with open(caminho, 'rb') as reads:
            digest = file_digest(reads, "sha256")
    except FileNotFoundError:
        return newprint(f'O arquivo do caminho {fore_cyan(caminho)} não foi encontrado', 'Verifique se o arquivo existe ou se o caminho está correto')
    except IsADirectoryError:
        return newprint(f'O caminho {fore_cyan(caminho)} está resultando em um diretório, não em um arquivo', 'Verifique se o caminho está completo')
    except PermissionError:
        return newprint(f'Permissão negada para acessar o arquivo do caminho {fore_cyan(caminho)}', 'Execute como administrador')
    except Exception as e:
        return print(f"    {Back.RED} Erro inesperado: {e}. {Back.RESET}")
    if space:
        return add_space(digest.hexdigest())
    return digest.hexdigest().upper()

def hash_pasta(diretorio, space = False):
    try:
        diretorio = Path(diretorio)
        if diretorio.exists() and diretorio.is_dir():
            hash_final = sha256()
            [hash_final.update(hash_arquivo(caminho_arquivo).encode('utf-8')) for caminho_arquivo in diretorio.rglob('*') if caminho_arquivo.is_file()]
            if space:
                return add_space(hash_final.hexdigest())
            return hash_final.hexdigest().upper()
        return newprint(f'O caminho {fore_cyan(diretorio)} não é um diretório ou não existe', 'Verifique se o caminho está correto')
    except Exception:
        return newprint(f'O caminho {fore_cyan(diretorio)} está vazia', 'Verifique se o caminho está correto ou maior do que o esperado')

def hash_a4a(caminho, space = False):
    try:
        caminho_dir = Path(caminho)
        if caminho_dir.exists() and caminho_dir.is_dir():
            archives = [f'[{arquivo.name}]: {hash_arquivo(str(arquivo.resolve()), space)}' for arquivo in caminho_dir.iterdir() if arquivo.is_file() and arquivo.name != 'hashs.txt']
            pastas = [str(diretorio.resolve()) for diretorio in caminho_dir.iterdir() if diretorio.is_dir() and diretorio.name != '__pycache__']
            if len(archives) != 0:
                with open(caminho + '/hashs.txt', 'w')  as f:  
                    [f.write(linha+'\n') for linha in archives]
            if len(pastas) != 0:
                [hash_a4a(pasta) for pasta in pastas]
            if len(pastas) + len(archives) < 1:
                return newprint(f'O caminho {fore_cyan(caminho)} está resultando em uma pasta vazia', 'Verifique se o caminho está correto')
            return True
        return newprint(f'O caminho {fore_cyan(caminho)} não existe ou não é uma pasta', 'Verifique se o caminho está correto ou se é, de fato, uma pasta')
    except Exception as e:
        return print(f"    {Back.RED} Erro inesperado: {e}. {Back.RESET}")
