from .db import Session, Request


class Cache:
    def get(self, currency_code, date):
        with Session() as session:
            query = session.query(Request).filter(Request.code == currency_code, Request.date == date).first()

            if query:
                return query.json
            else:
                return False

    def put(self, currency_code, date, json):
        with Session() as session:
            session.add(Request(currency_code, date, json))
            session.commit()
