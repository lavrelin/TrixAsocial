from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
from CORE.bot import bot
from DATABASE.base import get_session
from ANALYTICS.stats_collector import StatsCollector
from SERVICES.notification.admin_notifier import AdminNotifier

scheduler = AsyncIOScheduler()

async def send_daily_stats():
    """Отправка ежедневной статистики админам"""
    logger.info("📊 Отправка ежедневной статистики")
    
    async for session in get_session():
        stats_text = await StatsCollector.get_stats_text(session)
        await AdminNotifier.send_stats_notification(bot, stats_text)

def setup_scheduler():
    """Настройка планировщика задач"""
    # Ежедневная статистика в 00:00
    scheduler.add_job(
        send_daily_stats,
        trigger=CronTrigger(hour=0, minute=0),
        id='daily_stats',
        replace_existing=True
    )
    
    # TODO: Добавить другие задачи
    # - Очистка истекших кулдаунов
    # - Автопосты в каналы
    # - Резервное копирование
    
    scheduler.start()
    logger.info("✅ Планировщик задач запущен")

def shutdown_scheduler():
    """Остановка планировщика"""
    scheduler.shutdown()
    logger.info("🛑 Планировщик задач остановлен")
