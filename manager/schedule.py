# encoding: UTF-8
import datetime


class Schedule(object):
    def __init__(self, rooms, talks):
        self.rooms = rooms
        rooms.sort()
        self.talks = talks
        if self.talks:
            self.talks.sort()
            self.start_date = self.talks[0].start_date
            self.end_date = self.talks[-1].end_date
            self.total_minutes = int(
                ((self.end_date - self.start_date) + datetime.timedelta(hours=1)).total_seconds() / 60)
            self.size = self.total_minutes * 2
            self.reference_hours = self.calculate_reference_hours()
        self.load_template_data()

    def calculate_reference_hours(self):
        one_hour = datetime.timedelta(hours=1)
        first_hour = {'start': self.start_date, 'end': self.start_date + one_hour}
        first_hour['size'] = self.talk_size(first_hour['start'], first_hour['end'])
        hours = [first_hour]

        last_hour = hours[-1]['end']
        while last_hour.hour < self.end_date.hour:
            new_hour = {'start': last_hour, 'end': last_hour + one_hour}
            new_hour['size'] = self.talk_size(new_hour['start'], new_hour['end'])
            hours.append(new_hour)
            last_hour = new_hour['end']

        return hours

    def load_template_data(self):
        for room in self.rooms:
            room.talks = self.talks_for_room(room)

    def talks_for_room(self, room):
        room_talks = []
        date_anterior = self.start_date
        talks = [talk for talk in self.talks if talk.room == room]
        talks.sort()
        for talk in talks:
            if talk.start_date.time() > date_anterior.time():
                room_talks.append({'dummy': True, 'dummy_size': self.talk_size(date_anterior, talk.start_date)})
            talk.talk_size = self.talk_size(talk.start_date, talk.end_date)
            room_talks.append(talk)
            date_anterior = talk.end_date
        if talk.end_date.time() < self.end_date.time():
            room_talks.append({'dummy': True, 'dummy_size': self.talk_size(talk.end_date, self.end_date)})
        return room_talks

    def talk_size(self, start, end):
        minutes = int((end - start).total_seconds()) / 60
        return minutes * 100 / self.total_minutes
