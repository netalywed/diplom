from orders import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from django_rest_passwordreset.signals import reset_password_token_created

from backend.models import ConfirmEmailToken, User, Order, Contact


# не работает с джанго версией 4+
# new_user_registered = Signal(
#     providing_args=['user_id'],
# )
#
# new_order = Signal(
#     providing_args=['user_id'],
# )
# вместо этого ниже:

new_user_registered = Signal()
new_order = Signal()


@receiver(post_save, sender=Contact)
def send_email_after_address_added(sender, instance, created, **kwargs):
    if created:
        msg = EmailMultiAlternatives(
            # title:
            f"Delivery address for {instance.user.email}",
            # message:
            "You have successfully added a new delivery address!",
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [instance.user.email]
        )
        msg.send()


@receiver(post_save, sender=Order)
def send_email_after_order_confirmed(sender, instance, created, **kwargs):
    if created and instance.state == 'confirmed':
        for item in instance.ordered_items.all():
            msg = EmailMultiAlternatives(
                # title:
                f"New order",
                # message:
                f"You have a new order for produst {item.product_info.product.name}",
                # from:
                settings.EMAIL_HOST_USER,
                # to:
                [item.product_info.shop.user.email]
            )
            msg.send()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    # send an e-mail to the user

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {reset_password_token.user}",
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.send()


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    отправляем письмо с подтрердждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {token.user.email}",
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [token.user.email]
    )
    msg.send()


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Обновление статуса заказа",
        # message:
        'Заказ сформирован',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()
