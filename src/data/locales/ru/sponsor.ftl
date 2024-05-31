sponsor-expire-date-error=⚠️ Нельзя выбрать дату раньше текущей!
sponsor-invalid-id-error=⚠️ Вы ввели некорректный id!
sponsor-bot-access-error=⚠️ Бот должен быть администратором в канале спонсора!

sponsor-create-join-request=💡 Нужно ли переходе по ссылке отправлять запрос на вступление в канал?
sponsor-create-expire-date=🗓 До какой даты подписка на канал спонсора будет обязательной?
sponsor-create-channel-id=💡 Введите ID спонсорского канала или просто перешлите сообщение из него:
sponsor-create-success=✅ Спонсор успешно добавлен!

sponsor-delete-confirm=🤷🏻‍♂️ Вы уверены, что хотите удалить спонсора?

sponsor-update-title-success=✅ Название канала успешно обновлено!

sponsor-menu-view-all=📢 Вот все, добавленные каналы спонсоров:
sponsor-menu-view-one=<b>{{ sponsor.title }} ({{ sponsor.id }})\n</b>
 {% if sponsor.creates_join_request %}
 ✅ <b>Создаются</b> заявки на вступление в канал
 {% else %}
 ❌ Заявки на вступление в канал <b>не создаются</b>
 {% endif %}
 {% if sponsor.expire_date %}
 ⏳ Канал спонсора будет обязательным для подписки до <b>{{ sponsor.expire_date.date() }}</b>
 {% else %}
 ♾ Канал спонсора будет обязательным для подписки, <b>пока вы его не удалите</b>
 {% endif %}
sponsor-menu-view-one-deleted=❌ Канал был удалён!
sponsor-menu-go=✈️ Перейти в канал
sponsor-menu-update-title=🔄 Обновить название
sponsor-menu-invite-link=🔗 Новая ссылка
sponsor-menu-expire-date=🗓 Изменить срок действия
sponsor-menu-view-all=🔐 Для доступа к боту вы <b>должны</b> подписаться на <b>все</b> каналы из списка ниже:

sponsor-following-confirm=✅ Я подписался
sponsor-following-error=⚠️ Вы не подписались на каналы из списка!
sponsor-following-success=✅ Поздравляю! Теперь вы можете пользоваться ботом, введите /start!
