"""
# Observer Design Patten

==> Its a type of behavioral pattern that notify the change in state of one object to another object.

If one object behaviour depends on another object state then we have two ways to implement this communication.

Lets understand this by taking two objects

    obj_1 -> whose behaviour depends on state of another object.
    obj_2 -> whose change in state can effect the behaviour of other objects.

    Two ways of communication are - 
        1. obj_1 will keep on checking for state change in obj_2 to take action.
        2. obj_2 will inform the obj_1 upon any state changes.

    Out of these two strategies, it makes more sense to implement strategy 2 
    because it will save unncessary calls to obj_2 from obj_1.

==> Implementation

    There will be two interfaces - Publisher and Subscriber

    Publisher will maintain the list of subscribers to send notification upon any state changes.
    It can be simple array list of subscriber, upon which publisher can iterate and call for update method in
    each subscriber.

==> Usecase

    It will be used where we need to take certain actions upon any state changes in system.
    
    For example
    1. If we have to notify users on Email and SMS service when any new product is available on website for which they showed interest.
    2. Send Newsletter to subscribers when new post is published.
"""

from abc import ABC, abstractmethod
from typing import List
from random import randrange


class Subscriber(ABC):
    """
    Subscriber interface declaring update method used by publisher interface.
    """

    @abstractmethod
    def update(self, publisher: "Publisher") -> None:
        """
        Takes the action needed upon state changes in publisher
        """
        pass


class Publisher(ABC):
    @abstractmethod
    def add_subscriber(self, subscriber: Subscriber) -> None:
        """
        Add to subscriber list.
        """
        pass

    @abstractmethod
    def remove_subscriber(self, subscriber: Subscriber) -> None:
        """
        Remove from subscriber list.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify subscriber in list about state changes
        """
        pass


class ConcretePublisher(Publisher):

    def __init__(self) -> None:
        self._subscribers: List[Subscriber] = []
        self._new_products: int = 0

    def add_subscriber(self, subscriber: Subscriber) -> None:
        print("Publisher: Adding subscriber !")
        self._subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: Subscriber) -> None:
        print("Publisher: Removing subscriber !")
        self._subscribers.remove(subscriber)

    def notify(self) -> None:
        for subscriber in self._subscribers:
            subscriber.update(self)

    def business_logic(self) -> None:
        print("\nPublisher: Checking Inventory for new products!")
        self._new_products = randrange(0, 10)

        print(
            f"Publisher: My new products count has just changed to: {self._new_products}"
        )
        self.notify()


class SubscriberA(Subscriber):
    def update(self, publisher: Publisher) -> None:
        if publisher._new_products > 0:
            print("SubscriberA: Action Taken")


class SubscriberB(Subscriber):
    def update(self, publisher: Publisher) -> None:
        if publisher._new_products > 2:
            print("SubscriberA: Action Taken")


if __name__ == "__main__":

    # The client code.

    publisher = ConcretePublisher()

    sub_a = SubscriberA()
    sub_b = SubscriberB()

    publisher.add_subscriber(sub_a)
    publisher.add_subscriber(sub_b)

    publisher.business_logic()
    publisher.business_logic()
    publisher.business_logic()

    publisher.remove_subscriber(sub_a)

    publisher.business_logic()
    publisher.business_logic()
