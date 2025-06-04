from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai.llms import OpenAI
from pydantic import BaseModel, Field, field_validator

from langchain_community.document_loaders.sitemap import SitemapLoader

import nest_asyncio

nest_asyncio.apply()

sitemap_loader = SitemapLoader(web_path="https://mountainreview.com/page-sitemap.xml", verify_ssl=False)

docs = sitemap_loader.load()
print ("Read sitemap with", len(docs), "documents")

docs[0]

for (i, doc) in enumerate(docs):
    print(f"Document {i}:")
    print(f"  URL: {doc.metadata['source']}")


