import logging

from pkg.crm.domain.entities.discount_entity import DiscountEntity

logger = logging.getLogger(__name__)


class DiscountLogger:
    @staticmethod
    def log_creation(discount: DiscountEntity):
        logger.info(f"Discount created: {discount.name} ({discount.percentage}%)")

    @staticmethod
    def log_update(discount: DiscountEntity):
        logger.info(f"Discount updated: {discount.name} ({discount.percentage}%)")

    @staticmethod
    def log_deletion(discount: DiscountEntity):
        logger.info(f"Discount deleted: {discount.name}")
