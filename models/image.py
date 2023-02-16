class Image:
    def __init__(self, _id, additional_properties, address, alt_text, auth, caption, copyright, created_date,
                 creatorsFromString, credits, distributor, focal_point, geo, height, image_type, last_updated_date,
                 licensable, otherProps, owner, related_content, seo_filename, slug, source, status, subtitle, taxonomy,
                 type, url, version, width):
        self._id = _id
        self.additional_properties = additional_properties
        self.address = address
        self.alt_text = alt_text
        self.auth = auth
        self.caption = caption
        self.copyright = copyright
        self.created_date = created_date
        self.creatorsFromString = creatorsFromString
        self.credits = credits
        self.distributor = distributor
        self.focal_point = focal_point
        self.geo = geo
        self.height = height
        self.image_type = image_type
        self.last_updated_date = last_updated_date
        self.licensable = licensable
        self.otherProps = otherProps
        self.owner = owner
        self.related_content = related_content
        self.seo_filename = seo_filename
        self.slug = slug
        self.source = source
        self.status = status
        self.subtitle = subtitle
        self.taxonomy = taxonomy
        self.type = type
        self.url = url
        self.version = version
        self.width = width
