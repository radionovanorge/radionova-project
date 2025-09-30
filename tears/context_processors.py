from django.utils.timezone import localtime, now
from datetime import datetime
from .models import ProgramPage


def current_live_program(request):
    programs = ProgramPage.objects.live().all()
    current_time = localtime(now()).time()
    current_weekday = str(localtime(now()).isoweekday())  # 1 = Mandag, 7 = Søndag

    for program in programs:
        for block in program.sendetider:
            data = block.value
            weekday = data.get("weekday")
            if weekday == current_weekday:
                start_str = data.get("start_time")
                end_str = data.get("end_time")

                if start_str and end_str:
                    start = datetime.strptime(start_str, "%H:%M").time()
                    end = datetime.strptime(end_str, "%H:%M").time()
                    if start <= current_time <= end:
                        text = f"Direkte: Radio Nova / {start_str}–{end_str}: {program.title}"
                        return {"current_live_text": text}

    return {"current_live_text": None}
