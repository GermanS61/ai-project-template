#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"

ROOT = File.expand_path("../..", __dir__)
TEMPLATE_DIR = File.join(ROOT, ".github", "ISSUE_TEMPLATE")
FORM_TYPES = %w[checkboxes dropdown input markdown textarea upload].freeze
TOP_LEVEL_KEYS = %w[assignees body description labels name projects title type].freeze
CONFIG_KEYS = %w[blank_issues_enabled contact_links].freeze
CONTACT_LINK_KEYS = %w[about name url].freeze
STANDARD_BODY_KEYS = %w[attributes id type validations].freeze
MARKDOWN_BODY_KEYS = %w[attributes type].freeze
ATTRIBUTE_KEYS = {
  "checkboxes" => %w[description label options],
  "dropdown" => %w[default description label multiple options],
  "input" => %w[description label placeholder value],
  "markdown" => %w[value],
  "textarea" => %w[description label placeholder render value],
  "upload" => %w[description label]
}.freeze
VALIDATION_KEYS = {
  "checkboxes" => %w[required],
  "dropdown" => %w[required],
  "input" => %w[required],
  "markdown" => [],
  "textarea" => %w[required],
  "upload" => %w[accept required]
}.freeze
STRING_ATTRIBUTE_KEYS = {
  "checkboxes" => %w[description label],
  "dropdown" => %w[description label],
  "input" => %w[description label placeholder value],
  "markdown" => %w[value],
  "textarea" => %w[description label placeholder render value],
  "upload" => %w[description label]
}.freeze
ID_PATTERN = /\A[A-Za-z0-9_-]+\z/

def relative_path(path)
  path.delete_prefix("#{ROOT}/")
end

def non_empty_string?(value)
  value.is_a?(String) && !value.strip.empty?
end

def validate_allowed_keys(errors, location, mapping, allowed)
  unknown = mapping.keys.reject { |key| key.is_a?(String) && allowed.include?(key) }
  return if unknown.empty?

  errors << "#{location}: unknown keys: #{unknown.map(&:inspect).join(', ')}"
end

def validate_string_list(errors, path, document, field)
  return unless document.key?(field)

  value = document[field]

  valid = (value.is_a?(String) && value.split(",", -1).all? { |item| !item.strip.empty? }) ||
    (value.is_a?(Array) && value.all? { |item| non_empty_string?(item) })
  unless valid
    errors << "#{path}: '#{field}' must be a comma-delimited string or a list of non-empty strings"
  end
end

def normalized_label(label)
  label.downcase.gsub(/[^\p{Alnum}]+/u, "")
end

def register_reference(errors, references, location, label, id = nil)
  key = id ? "id:#{id}" : "label:#{normalized_label(label)}"
  if references.key?(key)
    errors << "#{location}: label/id reference '#{key}' duplicates #{references[key]}"
  else
    references[key] = location
  end
end

def validate_config(document, path, errors)
  unless document.is_a?(Hash)
    errors << "#{path}: the document root must be a mapping"
    return
  end

  validate_allowed_keys(errors, path, document, CONFIG_KEYS)

  if document.key?("blank_issues_enabled") && ![true, false].include?(document["blank_issues_enabled"])
    errors << "#{path}: 'blank_issues_enabled' must be true or false"
  end

  return unless document.key?("contact_links")

  links = document["contact_links"]
  unless links.is_a?(Array)
    errors << "#{path}: 'contact_links' must be a list"
    return
  end

  links.each_with_index do |link, index|
    location = "#{path}: contact_links[#{index}]"
    unless link.is_a?(Hash)
      errors << "#{location} must be a mapping"
      next
    end

    validate_allowed_keys(errors, location, link, CONTACT_LINK_KEYS)
    %w[name url about].each do |field|
      errors << "#{location}.#{field} must be a non-empty string" unless non_empty_string?(link[field])
    end
  end
end

def validate_string_attributes(errors, location, type, attributes)
  STRING_ATTRIBUTE_KEYS.fetch(type).each do |field|
    next unless attributes.key?(field)

    unless non_empty_string?(attributes[field])
      errors << "#{location}.attributes.#{field} must be a non-empty string"
    end
  end

  required = type == "markdown" ? "value" : "label"
  unless attributes.key?(required)
    errors << "#{location}.attributes.#{required} is required"
  end
end

def duplicate_values(values)
  values.group_by { |value| value }.select { |_value, matches| matches.length > 1 }.keys
end

def validate_dropdown_options(errors, location, attributes)
  options = attributes["options"]
  unless options.is_a?(Array) && !options.empty?
    errors << "#{location}.attributes.options must be a non-empty list"
    return
  end

  unless options.all? { |option| non_empty_string?(option) }
    errors << "#{location}: dropdown options must be non-empty strings"
  end

  string_options = options.select { |option| option.is_a?(String) }
  duplicates = duplicate_values(string_options)
  unless duplicates.empty?
    errors << "#{location}: dropdown options must be unique; duplicates: #{duplicates.map(&:inspect).join(', ')}"
  end

  if string_options.any? { |option| option.strip.casecmp("none").zero? }
    errors << "#{location}: dropdown options must not include the reserved word 'None'"
  end

  if attributes.key?("multiple") && ![true, false].include?(attributes["multiple"])
    errors << "#{location}.attributes.multiple must be true or false"
  end

  return unless attributes.key?("default")

  default = attributes["default"]
  unless default.is_a?(Integer)
    errors << "#{location}.attributes.default must be an integer option index"
    return
  end

  unless default.between?(0, options.length - 1)
    errors << "#{location}.attributes.default must reference an existing option index"
  end
  if string_options.any? { |option| option.strip.casecmp("n/a").zero? }
    errors << "#{location}: dropdown options with a default must not include 'n/a'"
  end
end

def validate_checkbox_options(errors, location, attributes, references)
  options = attributes["options"]
  unless options.is_a?(Array) && !options.empty?
    errors << "#{location}.attributes.options must be a non-empty list"
    return
  end

  options.each_with_index do |option, index|
    option_location = "#{location}.attributes.options[#{index}]"
    unless option.is_a?(Hash)
      errors << "#{option_location} must be a mapping"
      next
    end

    validate_allowed_keys(errors, option_location, option, %w[label required])
    label = option["label"]
    if non_empty_string?(label)
      register_reference(errors, references, option_location, label)
    else
      errors << "#{option_location}.label must be a non-empty string"
    end

    if option.key?("required") && ![true, false].include?(option["required"])
      errors << "#{option_location}.required must be true or false"
    end
  end
end

def validate_validations(errors, location, type, item)
  return unless item.key?("validations")

  validations = item["validations"]
  unless validations.is_a?(Hash)
    errors << "#{location}.validations must be a mapping"
    return
  end

  validate_allowed_keys(errors, "#{location}.validations", validations, VALIDATION_KEYS.fetch(type))
  if validations.key?("required") && ![true, false].include?(validations["required"])
    errors << "#{location}.validations.required must be true or false"
  end
  if validations.key?("accept") && !non_empty_string?(validations["accept"])
    errors << "#{location}.validations.accept must be a non-empty comma-delimited string"
  end
end

def validate_body_item(errors, path, item, index, ids, references)
  location = "#{path}: body[#{index}]"
  unless item.is_a?(Hash)
    errors << "#{location} must be a mapping"
    return
  end

  type = item["type"]
  unless FORM_TYPES.include?(type)
    errors << "#{location}.type must be one of: #{FORM_TYPES.join(', ')}"
    return
  end

  allowed_body_keys = type == "markdown" ? MARKDOWN_BODY_KEYS : STANDARD_BODY_KEYS
  validate_allowed_keys(errors, location, item, allowed_body_keys)

  attributes = item["attributes"]
  unless attributes.is_a?(Hash)
    errors << "#{location}.attributes must be a mapping"
    return
  end

  validate_allowed_keys(errors, "#{location}.attributes", attributes, ATTRIBUTE_KEYS.fetch(type))
  validate_string_attributes(errors, location, type, attributes)

  if type == "markdown"
    return
  end

  id = nil
  duplicate_id = false
  if item.key?("id")
    candidate = item["id"]
    if non_empty_string?(candidate) && ID_PATTERN.match?(candidate)
      id = candidate
      if ids.key?(id)
        errors << "#{location}.id duplicates '#{id}' from #{ids[id]}"
        duplicate_id = true
      else
        ids[id] = location
      end
    else
      errors << "#{location}.id must contain only letters, numbers, '-' or '_'"
    end
  end

  label = attributes["label"]
  register_reference(errors, references, location, label, id) if non_empty_string?(label) && !duplicate_id

  case type
  when "dropdown"
    validate_dropdown_options(errors, location, attributes)
  when "checkboxes"
    validate_checkbox_options(errors, location, attributes, references)
  end
  validate_validations(errors, location, type, item)
end

def validate_form(document, path, errors, form_names)
  unless document.is_a?(Hash)
    errors << "#{path}: the document root must be a mapping"
    return
  end

  validate_allowed_keys(errors, path, document, TOP_LEVEL_KEYS)

  %w[name description].each do |field|
    errors << "#{path}: '#{field}' must be a non-empty string" unless non_empty_string?(document[field])
  end
  if non_empty_string?(document["name"])
    name = document["name"]
    if form_names.key?(name)
      errors << "#{path}: form name '#{name}' duplicates #{form_names[name]}"
    else
      form_names[name] = path
    end
  end
  errors << "#{path}: 'title' must be a string" if document.key?("title") && !document["title"].is_a?(String)
  errors << "#{path}: 'type' must be a non-empty string" if document.key?("type") && !non_empty_string?(document["type"])
  validate_string_list(errors, path, document, "labels")
  validate_string_list(errors, path, document, "assignees")
  validate_string_list(errors, path, document, "projects")

  body = document["body"]
  unless body.is_a?(Array) && !body.empty?
    errors << "#{path}: 'body' must be a non-empty list"
    return
  end

  ids = {}
  references = {}
  body.each_with_index do |item, index|
    validate_body_item(errors, path, item, index, ids, references)
  end
  unless body.any? { |item| item.is_a?(Hash) && item["type"] != "markdown" }
    errors << "#{path}: 'body' must contain at least one non-markdown field"
  end
end

paths = Dir.glob(File.join(TEMPLATE_DIR, "*.{yml,yaml}")).sort
errors = []
form_names = {}

if paths.empty?
  errors << ".github/ISSUE_TEMPLATE: no YAML files found"
end

paths.each do |absolute_path|
  path = relative_path(absolute_path)
  begin
    content = File.read(absolute_path, encoding: "UTF-8")
    document = YAML.safe_load(
      content,
      permitted_classes: [],
      permitted_symbols: [],
      aliases: false,
      filename: path
    )
  rescue Psych::Exception, Encoding::InvalidByteSequenceError => e
    errors << "#{path}: invalid YAML: #{e.message.lines.first.strip}"
    next
  end

  if File.basename(absolute_path).match?(/\Aconfig\.ya?ml\z/)
    validate_config(document, path, errors)
  else
    validate_form(document, path, errors, form_names)
  end
end

unless errors.empty?
  warn errors.map { |error| "ERROR: #{error}" }.join("\n")
  exit 1
end

puts "Validated #{paths.length} Issue Form YAML files."
