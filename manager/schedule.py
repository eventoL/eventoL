# encoding: UTF-8


class Schedule(object):

    def __init__(self, rooms, talks):
        self.rooms = rooms
        self.talks = talks
        if self.talks:
            self.talks.sort()
            self.start_date = self.talks[0].start_date
            self.end_date = self.talks[-1].end_date
            self.minutes = (self.end_date.hour+1-self.start_date.hour)*60
            self.size = self.minutes*2
        self.load_template_data()

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
        minutes = (end.hour-start.hour)*60+end.minute-start.minute
        return minutes*100/self.minutes
