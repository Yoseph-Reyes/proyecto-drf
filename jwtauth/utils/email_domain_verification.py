from django.conf import settings

def verify_domain(email, domain):
    if "@" not in domain:
        raise ValueError("not valid domain, must include @ at the beggining")
    return email.endswith(domain)


def get_callback_url_domain(email):
    domains = {"@gmail.com": '@gmail.com'}
    result_domain = list(filter(lambda x: verify_domain(email, x), domains.keys()))
    if result_domain:
        return domains.get(result_domain[0])
