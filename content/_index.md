---
title: 
date: 2026-02-28
type: landing

sections:
  - block: hero
    content:
      title: CIRP Lab
      text: |
        Computational Imaging and Robotic Perception Lab<br>
        @ University of Hawaiʻi at Mānoa

        **AI · Robotics · Computer Vision**

        _Human-Centered AI in Motion_

        Think. Build. Interact.
      primary_action:
        text: Meet the Team
        url: ./people/
      secondary_action:
        text: View Publications
        url: ./publication/
    design:
      css_class: lab-hero
      background:
        color: '#070B14'
        image:
          filename: bg_1.png
          filters:
            brightness: 0.48
          size: cover
          position: top
      spacing:
        padding: ['90px', '0', '60px', '0']

  - block: markdown
    content:
      title: Research Themes
      text: |
        We engineer intelligent systems at the intersection of:

        - **AI for Perception and Interaction**: robust multimodal reasoning in the wild.
        - **Robotics for Real-World Deployment**: adaptive sensing and control under constraints.
        - **Computational Imaging Beyond RGB**: physics-informed vision with polarization, light transport, and optics.
    design:
      columns: '1'
      css_class: research-pillars
      spacing:
        padding: ['20px', '0', '30px', '0']

  - block: markdown
    content:
      title: Group Photos
      text: |
        {{< group_gallery >}}
    design:
      columns: '1'
      css_class: group-photos
      spacing:
        padding: ['20px', '0', '20px', '0']

  - block: markdown
    content:
      title: Latest News
      text: |
        {{< lab_news >}}
    design:
      css_class: news-tweets
      columns: '1'
      spacing:
        padding: ['20px', '0', '24px', '0']

  - block: collection
    content:
      title: Selected Publications
      text: ''
      count: 8
      filters:
        folders:
          - publication
      order: desc
    design:
      view: citation
      css_class: pub-feed
      columns: '1'

  - block: markdown
    content:
      title: Sponsors
      text: |
        {{< sponsors_grid >}}
    design:
      columns: '1'
      css_class: sponsors-strip
      spacing:
        padding: ['20px', '0', '50px', '0']
---
