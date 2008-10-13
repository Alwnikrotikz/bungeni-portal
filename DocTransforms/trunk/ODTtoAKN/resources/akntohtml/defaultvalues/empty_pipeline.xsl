<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:akn="http://www.akomantoso.org/1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    <xsl:output indent="yes" method="xml"/>

    <xsl:template match="/">
        <stylesheets>
            <xsl:apply-templates/>
        </stylesheets>
    </xsl:template>

    <xsl:template match="akn:*">
        <xsl:apply-templates />
    </xsl:template>

    <xsl:template match="text()">
        <xsl:apply-templates />
    </xsl:template>

<xsl:template match="to_replace"><XSLT_steps /></xsl:template>
</xsl:stylesheet>