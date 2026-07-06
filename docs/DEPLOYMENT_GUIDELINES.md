# Deployment Guidelines

## PyInstaller

- Build desktop oficial usa PyInstaller.
- Arquivos base: `build/build.py` e `build/build.spec`.
- Scripts: `scripts/build.ps1` e `scripts/build.sh`.

## Build Local

```powershell
.\scripts\build.ps1
```

```bash
./scripts/build.sh
```

## Estrutura de Release

- Executavel.
- Arquivo de configuracao.
- Pasta de logs.
- Banco local inicial ou migration automatizada.
- Notas de versao.

## Logs

- Logs ficam em `logs/`.
- Releases devem orientar coleta e envio seguro de logs.

## Banco Local

- SQLite e o alvo inicial.
- O arquivo de banco deve ficar fora do executavel.
- Migrations devem ser aplicadas antes do uso quando necessario.

## Backup e Restauracao

- Backup deve copiar banco e configuracoes.
- Restauracao deve validar versao do schema.
- Backups devem ser protegidos contra acesso indevido.

## Atualizacao

- Atualizacao deve preservar banco e configuracoes.
- Mudancas incompatveis devem ter roteiro de migracao.
