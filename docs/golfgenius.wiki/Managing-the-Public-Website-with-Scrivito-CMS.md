# Getting started

Go to Admin > System and Marketing CMS > Edit Public Site

If possible, test changes on a test server like ggstest2 before applying them to production. (https://ggstest2.com/scrivito/)

A GolfGenius homepage should open in a Scrivito sandbox. A new menubar will pop-up on the right side of the menu. **Click the burger menu icon and select Start tour.**

This how the menu should look after completing these steps:

<img width="1890" alt="Screen Shot 2020-10-30 at 10 33 58" src="https://user-images.githubusercontent.com/16760229/97677762-77608780-1a9b-11eb-9571-75f7ab7b2a24.png">

# How Scrivito Works

Scrivito organizes content into pages containing widgets. A widget can be copied across multiple pages and reconfigured.

Text can be edited directly on the page by clicking on it.

When hovering over a widget, you are given options to add new widgets next to it or configure the widget.

<img width="697" alt="Screen Shot 2020-10-30 at 10 36 50" src="https://user-images.githubusercontent.com/16760229/97678019-d58d6a80-1a9b-11eb-8467-680613bf4fb8.png">

Scrivito is also integrated into Rails and we can create new content programmatically, while also keeping the Scrivito edit functionality. To do this, use the `scrivito_tag` function in .haml files to use text managed by Scrivito.

An example of this is the subtitle on the main page.

```haml
%h1.headline
  Less Work.
  %br/
  More Fun.
  %br/
  More Revenue.
  = scrivito_tag(:h3, @obj, :subtitle)
```

# Create a new component

1. Under `app/lib/cms/` directory a new class should be created which is the Scrivito object to work with.
Example: `my_name_widget.rb`, `my_name_page.rb`.
This class needs to inherit from one of the following base classes: `Cms::Widget`, `Cms::Page`, `Cms::Obj` depending on the functionality of the component. Here we will have the attributes and the specific methods for this component. A default method that should be present is `self.description_for_editor` which is the description displayed in Scrivito editor.

```ruby
class Cms::GlobalStatsWidget < Cms::Widget

  def self.description_for_editor
    "Global Stats with Map Background"
  end
end
```

2. Under `app/views/cms/` directory a new folder should be created withe the name of the component. Example: `my_component_name`. This folder will contain three files at all time. 
* `details.html.haml` will contain the scrivito tags used to edit the component in Edit Mode. This is the file that links the input from the user in Scrivito editor and the attributes of the component. Example:

```haml
= scrivito_details_for("Action") do
 = scrivito_tag(:div, widget, :action_link)
```
* `show.html.haml` (for widgets) or `index.html.haml` (for pages) will contain the layout for the component.

* `thumbnail.html.haml` will contain the render for the Scrivito thumbnail.
Example: 
```haml
= render("cms/thumbnail", obj_class: Cms::CallToActionWidget)
```

3. Under `app/assets/stylesheets/public_v4/` directory a new style file will be created which will contain the style for the component. Example: `my_name_widget.sass`


# FAQ

