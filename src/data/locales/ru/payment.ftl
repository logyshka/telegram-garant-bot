payment-account-connected=⚠️ Аккаунт платёжной системы успешно подключен
payment-account-absent=⚠️ Вы не подключили аккаунт платёжной системы
payment-unknown-error=⚠️ Данная система не подключена в коде
payment-amount-invalid=⚠️ Введена некорректная сумма

payment-settings-choice=<b>⚙️ Выберите платёжную систему для настройки:</b>
payment-settings-list-view={% if item[1] %}✅{% else %}❌{% endif %} {{ item[0].display_name }}
payment-settings-item-view=<b>{% if state %}✅{% else %}❌{% endif %} {{ payment.display_name }}\n</b>
 {% if state %}
 {% for field in fields %}
 <i>{{ field.name }}{{ field.sep }}{{ field.value }}</i>
 {% endfor %}
 {% endif %}
payment-settings-item-change=📲 {% if has_account %}Подключить другой аккаунт{% else %}Подключить аккаунт{% endif %}

bill-create-currency=💵 Выберите валюту для пополнения:
bill-create-amount=💵 Введите сумму пополнения от <b>{{ limits.min_str }}</b> до <b>{{ limits.max_str }}</b>
bill-create-payment=💡 Выберите способ пополнения:
bill-pending=💳 Способ пополнения: <b>{{ bill.payment_display_name }}</b>
 💵 Сумма пополнения <b>{{ bill.amount_str }}</b>
 <b><a href='{{ bill.pay_url }}'>🔗 Перейти к оплате (кликабельно)</a></b>
bill-pay-url=🔗 Перейти к оплате
bill-check=✅ Я оплатил
bill-paid=✅ Ваш баланс был пополнен на <b>{bill.amount} {bill.currency}</b>
bill-non-paid=❌ Счёт не был оплачен!
bill-cancelled=✅ Счёт был успешно отменён!

payment-crypto-bot-token-error=⚠️ Введённый токен недействителен
payment-crypto-bot-token-input=💡 Введите API токен, полученный в @CryptoBot:
