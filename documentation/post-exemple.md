# Working POST exemple

```xml
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
<record>
<header>
 <identifier>oai:FakeArXiv.org:1234.5678</identifier>
 <datestamp>2022-01-01</datestamp>
 <setSpec>cs</setSpec>
</header>
<metadata>
 <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
 <dc:title>Fake Title</dc:title>
 <dc:creator>Fake, Author A.</dc:creator>
 <dc:subject>Computer Science - Fake Subject</dc:subject>
 <dc:description> This is a fake description for debugging purposes. </dc:description>
 <dc:description> This is a comment. </dc:description>
 <dc:date>2022-01-02</dc:date>
 <dc:date>2022-01-03</dc:date>
 <dc:type>text</dc:type>
 <dc:identifier>http://fakearxiv.org/abs/1234.5678</dc:identifier>
 </oai_dc:dc>
</metadata>
</record>
</OAI-PMH>""",
"""
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
<record>
<header>
 <identifier>oai:FakeArXiv.org:2345.6789</identifier>
 <datestamp>2022-01-01</datestamp>
 <setSpec>cs</setSpec>
</header>
<metadata>
 <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
 <dc:title>Fake Title</dc:title>
 <dc:creator>Fake, Author B.</dc:creator>
 <dc:subject>Computer Science - Fake Subject</dc:subject>
 <dc:description> This is a fake description for debugging purposes. </dc:description>
 <dc:description> This is a comment. </dc:description>
 <dc:date>2022-01-02</dc:date>
 <dc:date>2022-01-03</dc:date>
 <dc:type>text</dc:type>
 <dc:identifier>http://fakearxiv.org/abs/2345.6789</dc:identifier>
 </oai_dc:dc>
</metadata>
</record>
</OAI-PMH>
```

```xml
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
<record>
<header>
 <identifier>oai:FakeArXiv.org:3456.7890</identifier>
 <datestamp>2022-01-02</datestamp>
 <setSpec>physic</setSpec>
</header>
<metadata>
 <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
 <dc:title>Fake Title</dc:title>
 <dc:creator>Fake, Author B.</dc:creator>
 <dc:subject>Physic - Fake Subject</dc:subject>
 <dc:description> This is a fake description for debugging purposes. </dc:description>
 <dc:description> This is a comment. </dc:description>
 <dc:date>2022-01-04</dc:date>
 <dc:date>2022-01-05</dc:date>
 <dc:type>text</dc:type>
 <dc:identifier>http://fakearxiv.org/abs/3456.7890</dc:identifier>
 </oai_dc:dc>
</metadata>
</record>
</OAI-PMH>
```

```xml
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
<record>
<header>
 <identifier>oai:arXiv.org:1004.3608</identifier>
 <datestamp>2021-03-22</datestamp>
 <setSpec>cs</setSpec>
</header>
<metadata>
 <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
 <dc:title>Mock Title</dc:title>
 <dc:creator>Mock Creator</dc:creator>
 <dc:subject>Mock Subject</dc:subject>
 <dc:subject>Mock Subject</dc:subject>
 <dc:subject>Mock Subject</dc:subject>
 <dc:subject>Mock Subject</dc:subject>
 <dc:subject>Mock Subject</dc:subject>
 <dc:description>Mock Description</dc:description>
 <dc:description>Mock Description</dc:description>
 <dc:date>2021-03-23</dc:date>
 <dc:date>2021-03-24</dc:date>
 <dc:type>text</dc:type>
 <dc:identifier>http://arxiv.org/abs/1004.3609</dc:identifier>
 <dc:identifier>Mock Identifier</dc:identifier>
 </oai_dc:dc>
</metadata>
</record>
```

```xml
</OAI-PMH>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
<record>
<header>
 <identifier>oai:arXiv.org:1004.3609</identifier>
 <setSpec>cs</setSpec>
</header>
<metadata>
 <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
 <dc:title>Mock Title1</dc:title>
 <dc:creator>Mock Creator</dc:creator>
 <dc:subject>Mock Subject1</dc:subject>
 <dc:subject>Mock Subject2</dc:subject>
 <dc:subject>Mock Subject3</dc:subject>
 <dc:subject>Mock Subject4</dc:subject>
 <dc:subject>Mock Subject5</dc:subject>
 <dc:description>Mock Description1</dc:description>
 <dc:description>Mock Description2</dc:description>
 <dc:date>2021-03-23</dc:date>
 <dc:date>2021-03-24</dc:date>
 <dc:type>text</dc:type>
 </oai_dc:dc>
</metadata>
</record>
</OAI-PMH>
```