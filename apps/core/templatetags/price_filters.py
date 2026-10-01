from django import template

register = template.Library()


@register.filter
def indian_price(value):
    try:
        price = float(value)
    except (ValueError, TypeError):
        return value

    if price >= 10000000:
        crore = price / 10000000

        if crore == int(crore):
            return f"{int(crore)} Cr"

        return f"{crore:.2f}".rstrip("0").rstrip(".") + " Cr"

    elif price >= 100000:
        lakh = price / 100000

        if lakh == int(lakh):
            return f"{int(lakh)} Lakh"

        return f"{lakh:.2f}".rstrip("0").rstrip(".") + " Lakh"

    else:
        return f"{int(price):,}"