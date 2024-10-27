from data_sources.bazos_sk.formatters.email.bazos_sk_email_formatter import BazosSkEmailFormatter

FORMATTERS: dict[str, type] = {
    'email_formatter': BazosSkEmailFormatter
}