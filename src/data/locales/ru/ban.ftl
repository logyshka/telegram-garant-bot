ban-create-reason=Введите причину бана или нажмите пропустить для того, забанить пользователя без указания причины:
ban-create-reason-error=Максимальная длина причины {max}
ban-create-till=Введите длительность бана в секундах или нажмите пропустить для того, чтобы забанить пользователя навсегда:
ban-create-till-error=Минимальное время бана в секундах: {min}
ban-create-confirm=Пользователь <code>#{{ user_id }}</code> будет забанен {% if reason %} по причине <code>"{{ reason }}"</code>{% else %} <code>без указания причины</code> {% endif %} {% if till %} <b>до {{ till }}</b> {% else %} <b>навсегда</b> {% endif %}
ban-create-success=Пользователь успешно забанен!

ban-delete-confirm=Вы уверены, что хотите разбанить пользователя <code>{{ user_id }}</code>
ban-delete-success=Пользователь успешно разбанен!

ban-user-banned=Пользователь <code>#{{ user_id }}</code> забанен {% if ban.reason %} по причине <code>"{{ ban.reason }}"</code>{% else %} <code>без указания причины</code> {% endif %} {% if ban.till %} <b>до {{ ban.till }}</b> {% else %} <b>навсегда</b> {% endif %}
ban-user-unbanned=Пользователь <code>#{{ user_id }}</code> не забанен

ban=🖤 Забанить
unban=❤️ Разбанить
