```
  #tabs.btsp_custom_tabs
    %nav.navbar.navbar-default
      .navbar-header
        %button.navbar-toggle.collapsed.pull_left.open_settings_menu{"aria-expanded" => "false", 
        "data-target" => "#all-tabs", "data-toggle" => "collapse", :type => "button"}
          %span
            %i.fa.fa-caret-down
            %span.extra_text= "Round Profile Sections"
          %span.sr-only
      #all-tabs.collapse.navbar-collapse.btsp_custom_tabs_menu
        %ul.nav.navbar-nav.nav-center
          %li= link_to "General Settings", "#tabs1"
          %li= link_to "Handicap Settings", "#tabs3"
          %li= link_to "Signups & Scheduling", "#tabs2"
          %li= link_to "Tournaments & Scoring", "#tabs4"
          %li= link_to "More Info", "#tabs5"
    .btsp_ps_container.btsp_custom_tabs_container
      .row
        .col-xs-12.col-sm-11.col-md-11.col-lg-11.col-sm-offset-1.col-md-offset-1.col-lg-offset-1.tabs_content.btsp_form_content
          = render partial: "rounds/tabs/tabs1", locals: {f: f}
          = render partial: "rounds/tabs/tabs2", locals: {f: f}
          = render partial: "rounds/tabs/tabs3", locals: {f: f}
          = render partial: "rounds/tabs/tabs4", locals: {f: f}
          = render partial: "rounds/tabs/tabs5", locals: {f: f}
```