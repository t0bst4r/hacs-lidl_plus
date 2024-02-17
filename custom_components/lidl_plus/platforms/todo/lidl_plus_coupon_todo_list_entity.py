from __future__ import annotations

import datetime

from homeassistant.components.todo import (
    TodoItem,
    TodoItemStatus,
    TodoListEntity, TodoListEntityFeature,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...data import LidlPlusDataUpdateCoordinator
from ...domain import LidlPlusData


class LidlPlusCouponTodoListEntity(CoordinatorEntity[LidlPlusDataUpdateCoordinator], TodoListEntity):
    _attr_icon = "mdi:ticket-percent"
    _attr_has_entity_name = True
    _attr_supported_features = (
            TodoListEntityFeature.UPDATE_TODO_ITEM
            | TodoListEntityFeature.SET_DUE_DATETIME_ON_ITEM
            | TodoListEntityFeature.SET_DESCRIPTION_ON_ITEM
    )

    def __init__(self, coordinator: LidlPlusDataUpdateCoordinator, unique_id: str) -> None:
        super().__init__(coordinator)
        self._list_uuid = "coupons"
        self._attr_name = "Coupons"
        self._attr_unique_id = f"{unique_id}_{self._list_uuid}"

    @property
    def todo_items(self) -> list[TodoItem]:
        return [
            TodoItem(
                uid=item.id,
                summary=item.title,
                description=f"{item.offerTitle} | {item.offerDescription} | {item.section}",
                status=TodoItemStatus.COMPLETED if item.isActive else TodoItemStatus.NEEDS_ACTION,
                due=datetime.datetime.fromisoformat(item.endValidityDate)
            )
            for item in self.lidl_plus_data.coupons.values()
        ]

    @property
    def lidl_plus_data(self) -> LidlPlusData:
        return self.coordinator.data

    async def async_create_todo_item(self, item: TodoItem) -> None:
        raise HomeAssistantError("You cannot create new coupons")

    async def async_update_todo_item(self, item: TodoItem) -> None:
        prev_item = self.lidl_plus_data.coupons[item.uid]
        if item.status == TodoItemStatus.COMPLETED:
            if not prev_item.isActive:
                await self.hass.async_add_executor_job(self.coordinator.lidl.activate_coupon, item.uid)
                prev_item.isActive = True
        else:
            if prev_item.isActive:
                await self.hass.async_add_executor_job(self.coordinator.lidl.deactivate_coupon, item.uid)
                prev_item.isActive = False
        await self.coordinator.async_refresh()

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        raise HomeAssistantError("You cannot delete a coupon")
