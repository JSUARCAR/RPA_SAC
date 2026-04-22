# Configuración

## Archivo config.ini

```ini
[Paths]
source_excel_path = C:\ruta\a\Control_PQR.xlsx
dest_dir = C:\Users\Download
```

## Credenciales en Excel

Las credenciales se almacenan en la hoja `PARAMETROS_LOCALES`:

| Celda | Contenido |
|-------|-----------|
| M2 | Usuario SAC |
| N2 | Contraseña SAC |

## Rutas de Anexos

| Celda | Contenido |
|-------|-----------|
| K2 | Ruta de correos descargados |
| K3 | Ruta de anexos Mercurio |

## URLs del Sistema

| Variable | URL |
|----------|-----|
| sac_url | https://sac.corp.epm.com.co/GEN/Vistas/Login/LOGIN_GEN.aspx |
| sac_admin_url | https://sac.corp.epm.com.co/SAC/Vistas/App/PRO_ADMPRO.aspx |
