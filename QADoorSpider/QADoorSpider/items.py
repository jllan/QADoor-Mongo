from scrapy import Item, Field


class QuestionItem(Item):
    _id = Field()
    url = Field()
    title = Field()
    content = Field()
    is_solved = Field()
    answer_count = Field()
    view_count = Field()
    vote_count = Field()
    answers = Field()
    tags = Field()
    source = Field()