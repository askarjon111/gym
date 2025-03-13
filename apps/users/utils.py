from apps.controls.models import Gym
from apps.users.models import Access, User
from apps.users.tasks import generate_and_save_access


def get_user_access(user: User, gym: Gym) -> Access:
    access = user.access.filter(gym=gym).last()
    if not access:
        access = generate_and_save_access(user.id, gym.id)
    return access
