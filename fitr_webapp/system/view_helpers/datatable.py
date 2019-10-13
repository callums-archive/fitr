from flask import (
    abort
)

from . import Base

from datetime import datetime

from flask import jsonify


class Datatable(Base):

    def __init__(self):
        super(Datatable, self).__init__()

    def datatable(self):
        sort_col = self.columns()[int(
            self.request.args.get("order[0][column]"))]
        sort_dir = "+" if self.request.args.get(
            "order[0][dir]") == "asc" else "-"

        model = self.model()
        record_total = model.count()
        if len(self.request.args.get("search[value]", "")) > 0:
            model = self.search(self.request.args.get("search[value]"))

        model = model.order_by(sort_dir + sort_col).limit(
            int(self.request.args.get('length', 10))
        ).skip(
            int(self.request.args.get('start', 0))
        )

        data = []
        fields = self.columns()

        for record in model:
            row = {}
            for field in fields:
                if hasattr(record, field):
                    row[field] = getattr(record, field)
            data.append(row)

        return jsonify({
            "draw": int(self.request.args.get('draw', 1)),
            "recordsTotal": record_total,
            "recordsFiltered": len(data) if len(self.request.args.get("search[value]", "")) > 0 else record_total,
            "data": data
        })
