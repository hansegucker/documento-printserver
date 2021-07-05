from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DOCUMENTO_PRINTSERVER",
    settings_files=["/etc/documento/printserver/settings.toml"],
)
