# Widgets and Actions Reference

Complete reference for ChatKit widgets and action handling.

## Widget Overview

Widgets are rich UI components that can be streamed into the chat. They support:
- Interactive elements (buttons, forms, selects)
- Actions that trigger server-side logic
- Dynamic updates and replacements

## Widget Types

### Layout Widgets

#### Box

Container with padding and styling:

```python
from chatkit.widgets import Box, Text

widget = Box(
    padding="md",
    background="surface",
    children=[
        Text(content="Content inside box"),
    ]
)
```

#### Row

Horizontal layout:

```python
from chatkit.widgets import Row, Button

widget = Row(
    gap="sm",
    align="center",
    children=[
        Button(label="Option A", action="select", payload={"choice": "a"}),
        Button(label="Option B", action="select", payload={"choice": "b"}),
    ]
)
```

#### Col

Vertical layout:

```python
from chatkit.widgets import Col, Text

widget = Col(
    gap="md",
    children=[
        Text(content="First item"),
        Text(content="Second item"),
    ]
)
```

#### Divider

Visual separator:

```python
from chatkit.widgets import Divider

widget = Divider(margin="lg")
```

### Display Widgets

#### Text

Plain or styled text:

```python
from chatkit.widgets import Text

# Plain text
widget = Text(content="Hello world")

# Styled text
widget = Text(
    content="Important notice",
    weight="bold",
    size="lg",
    color="primary",
)
```

#### Markdown

Rendered markdown content:

```python
from chatkit.widgets import Markdown

widget = Markdown(
    content="""
# Heading

This is **bold** and _italic_.

- List item 1
- List item 2

```python
print("code block")
```
"""
)
```

#### Card

Container with title and optional actions:

```python
from chatkit.widgets import Card, Text, Button

widget = Card(
    title="Flight Details",
    subtitle="BA 123 - London to New York",
    children=[
        Text(content="Departure: 10:00 AM"),
        Text(content="Arrival: 2:00 PM EST"),
    ],
    footer=[
        Button(label="Change Flight", action="change_flight"),
        Button(label="Cancel", action="cancel_flight", variant="secondary"),
    ]
)
```

#### Image

Display images:

```python
from chatkit.widgets import Image

widget = Image(
    src="https://example.com/image.jpg",
    alt="Description of image",
    width=300,
    height=200,
)
```

#### Icon

Display icons:

```python
from chatkit.widgets import Icon

widget = Icon(
    name="check-circle",
    size="lg",
    color="success",
)
```

### Interactive Widgets

#### Button

Clickable button with action:

```python
from chatkit.widgets import Button

# Primary button
widget = Button(
    label="Submit",
    action="submit_form",
    payload={"form_id": "contact"},
)

# Secondary button
widget = Button(
    label="Cancel",
    action="cancel",
    variant="secondary",
)

# Icon button
widget = Button(
    label="Settings",
    action="open_settings",
    icon="settings",
)

# Disabled button
widget = Button(
    label="Processing...",
    action="submit",
    disabled=True,
)
```

#### Select

Dropdown selection:

```python
from chatkit.widgets import Select, SelectOption

widget = Select(
    placeholder="Choose an option",
    action="select_option",
    options=[
        SelectOption(label="Option 1", value="opt1"),
        SelectOption(label="Option 2", value="opt2"),
        SelectOption(label="Option 3", value="opt3", disabled=True),
    ]
)
```

#### Input

Text input field:

```python
from chatkit.widgets import Input

widget = Input(
    placeholder="Enter your name",
    action="input_name",
    type="text",  # "text", "email", "password", "number"
)
```

#### Textarea

Multi-line text input:

```python
from chatkit.widgets import Textarea

widget = Textarea(
    placeholder="Enter your message",
    action="input_message",
    rows=4,
)
```

#### Checkbox

Toggle checkbox:

```python
from chatkit.widgets import Checkbox

widget = Checkbox(
    label="I agree to the terms",
    action="toggle_agreement",
    checked=False,
)
```

#### RadioGroup

Radio button group:

```python
from chatkit.widgets import RadioGroup, RadioOption

widget = RadioGroup(
    action="select_plan",
    options=[
        RadioOption(label="Basic - $9/mo", value="basic"),
        RadioOption(label="Pro - $29/mo", value="pro"),
        RadioOption(label="Enterprise - Custom", value="enterprise"),
    ]
)
```

#### DatePicker

Date selection:

```python
from chatkit.widgets import DatePicker

widget = DatePicker(
    action="select_date",
    placeholder="Select a date",
    min_date="2024-01-01",
    max_date="2025-12-31",
)
```

### Form Widgets

#### Form

Group inputs with submit action:

```python
from chatkit.widgets import Form, Input, Select, Button, Col

widget = Form(
    action="submit_booking",
    children=[
        Col(
            gap="md",
            children=[
                Input(name="name", placeholder="Your name", required=True),
                Input(name="email", placeholder="Email", type="email", required=True),
                Select(
                    name="room_type",
                    placeholder="Room type",
                    options=[
                        SelectOption(label="Single", value="single"),
                        SelectOption(label="Double", value="double"),
                    ]
                ),
                Button(label="Book Now", type="submit"),
            ]
        )
    ]
)
```

### List Widgets

#### List

Display list of items:

```python
from chatkit.widgets import List, ListItem

widget = List(
    children=[
        ListItem(
            title="John Doe",
            subtitle="john@example.com",
            action="select_user",
            payload={"user_id": "123"},
        ),
        ListItem(
            title="Jane Smith",
            subtitle="jane@example.com",
            action="select_user",
            payload={"user_id": "456"},
        ),
    ]
)
```

## Actions

Actions let widgets trigger server-side logic without sending a user message.

### ActionConfig

Attach actions to interactive widgets:

```python
from chatkit.widgets import Button, ActionConfig

widget = Button(
    label="Confirm",
    action=ActionConfig(
        type="confirm_booking",
        payload={"booking_id": "B123"},
    )
)
```

### Handling Actions on Server

Override the `action` method in your ChatKitServer:

```python
class MyChatKitServer(ChatKitServer):
    async def action(
        self,
        thread: ThreadMetadata,
        action_type: str,
        payload: dict,
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        if action_type == "confirm_booking":
            booking_id = payload.get("booking_id")

            # Perform action
            result = await confirm_booking(booking_id)

            # Stream response
            yield ThreadItemAddedEvent(
                item=AssistantMessageItem(
                    id=await self.store.generate_id("msg"),
                    content=[TextContent(text=f"Booking {booking_id} confirmed!")],
                )
            )
            yield ThreadItemDoneEvent(id=item.id)

        elif action_type == "select_option":
            option = payload.get("value")

            # Update widget in place
            yield ThreadItemReplacedEvent(
                id=payload.get("widget_id"),
                item=create_updated_widget(option),
            )

        elif action_type == "cancel":
            # Remove widget
            yield ThreadItemRemovedEvent(id=payload.get("widget_id"))
```

### Action Patterns

#### Button Actions

```python
# Simple action
Button(label="Click me", action="button_clicked")

# Action with payload
Button(
    label="Delete",
    action="delete_item",
    payload={"item_id": "123"},
)

# Confirmation action
Button(
    label="Delete Account",
    action="delete_account",
    confirm="Are you sure? This cannot be undone.",
)
```

#### Form Actions

```python
# Form submission
Form(
    action="submit_contact_form",
    children=[
        Input(name="name", placeholder="Name"),
        Input(name="email", placeholder="Email", type="email"),
        Textarea(name="message", placeholder="Message"),
        Button(label="Send", type="submit"),
    ]
)

# Server handling
async def action(self, thread, action_type, payload, context):
    if action_type == "submit_contact_form":
        name = payload.get("name")
        email = payload.get("email")
        message = payload.get("message")

        # Process form
        await save_contact(name, email, message)

        # Respond
        yield ThreadItemAddedEvent(item=...)
```

#### Selection Actions

```python
# Dropdown selection
Select(
    action="select_category",
    options=[
        SelectOption(label="Tech", value="tech"),
        SelectOption(label="Business", value="business"),
    ]
)

# Multi-select
Select(
    action="select_tags",
    multiple=True,
    options=[
        SelectOption(label="Python", value="python"),
        SelectOption(label="JavaScript", value="javascript"),
        SelectOption(label="Rust", value="rust"),
    ]
)
```

## Streaming Widgets

### From Agent Tools

Stream widgets from within agent tools:

```python
from agents import function_tool
from chatkit.agents import AgentContext
from chatkit.widgets import Card, Text, Button

@function_tool
async def show_product(
    context: RunContextWrapper[AgentContext],
    product_id: str,
) -> str:
    """Display product details."""
    ctx = context.context
    product = await get_product(product_id)

    widget = Card(
        title=product.name,
        subtitle=f"${product.price}",
        children=[
            Text(content=product.description),
        ],
        footer=[
            Button(
                label="Add to Cart",
                action="add_to_cart",
                payload={"product_id": product_id},
            ),
        ]
    )

    ctx.stream_widget(widget, copy_text=f"{product.name} - ${product.price}")

    return f"Showing product: {product.name}"
```

### From respond()

Stream widgets directly from respond:

```python
async def respond(self, thread, input, context):
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

    # Show welcome widget for new threads
    if not input:
        widget = Card(
            title="Welcome!",
            children=[
                Text(content="How can I help you today?"),
            ],
            footer=[
                Button(label="Get Started", action="get_started"),
                Button(label="View Help", action="view_help"),
            ]
        )
        agent_context.stream_widget(widget)
        return

    # Continue with agent response
    async for event in stream_agent_response(agent_context, result):
        yield event
```

## Widget Updates

### Replacing Widgets

Update a widget in place:

```python
async def action(self, thread, action_type, payload, context):
    if action_type == "toggle_details":
        widget_id = payload.get("widget_id")
        expanded = payload.get("expanded", False)

        # Create updated widget
        updated = create_details_widget(expanded=not expanded)
        updated.id = widget_id  # Keep same ID

        yield ThreadItemReplacedEvent(id=widget_id, item=updated)
```

### Removing Widgets

Remove a widget from the thread:

```python
async def action(self, thread, action_type, payload, context):
    if action_type == "dismiss_notification":
        widget_id = payload.get("widget_id")
        yield ThreadItemRemovedEvent(id=widget_id)
```

## Client Effects

Trigger client-side behavior without UI changes:

```python
from chatkit.types import ClientEffectEvent

# Open external link
yield ClientEffectEvent(
    type="open_url",
    payload={"url": "https://example.com"},
)

# Show toast notification
yield ClientEffectEvent(
    type="toast",
    payload={"message": "Item saved!", "type": "success"},
)

# Focus element
yield ClientEffectEvent(
    type="focus",
    payload={"element_id": "search-input"},
)

# Custom effect (handled by frontend)
yield ClientEffectEvent(
    type="sync_map",
    payload={"station_id": "123"},
)
```

## Best Practices

### Widget Design

1. **Keep widgets focused**: One primary action per widget
2. **Provide feedback**: Update or replace widgets after actions
3. **Handle errors gracefully**: Show error states in widgets
4. **Consider mobile**: Test widgets on small screens

### Action Handling

1. **Validate payloads**: Never trust action payloads blindly
2. **Idempotency**: Make actions safe to retry
3. **Progress indication**: Show loading states for slow actions
4. **Error responses**: Return helpful error messages

### Performance

1. **Lazy load**: Don't stream all widgets at once
2. **Pagination**: Use lists with load-more actions
3. **Caching**: Cache widget data when appropriate

## Complete Example

```python
from chatkit.server import ChatKitServer
from chatkit.widgets import Card, Text, Button, Row, List, ListItem
from chatkit.types import ThreadStreamEvent, ThreadItemAddedEvent, ThreadItemDoneEvent

class ProductChatServer(ChatKitServer):
    async def respond(self, thread, input, context):
        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

        # Check for product search intent
        if input and "show products" in input.content[0].text.lower():
            products = await get_products()

            widget = Card(
                id=await self.store.generate_id("widget"),
                title="Available Products",
                children=[
                    List(
                        children=[
                            ListItem(
                                title=p.name,
                                subtitle=f"${p.price}",
                                action="view_product",
                                payload={"product_id": p.id},
                            )
                            for p in products[:5]
                        ]
                    ),
                ],
                footer=[
                    Button(label="Load More", action="load_more_products"),
                ]
            )

            agent_context.stream_widget(widget)
            yield ThreadItemDoneEvent(id=widget.id)
            return

        # Default agent response
        async for event in stream_agent_response(agent_context, result):
            yield event

    async def action(self, thread, action_type, payload, context):
        if action_type == "view_product":
            product = await get_product(payload["product_id"])

            widget = Card(
                id=await self.store.generate_id("widget"),
                title=product.name,
                children=[
                    Text(content=product.description),
                    Text(content=f"Price: ${product.price}", weight="bold"),
                ],
                footer=[
                    Row(
                        children=[
                            Button(
                                label="Add to Cart",
                                action="add_to_cart",
                                payload={"product_id": product.id},
                            ),
                            Button(
                                label="Back",
                                action="show_products",
                                variant="secondary",
                            ),
                        ]
                    )
                ]
            )

            yield ThreadItemAddedEvent(item=widget)
            yield ThreadItemDoneEvent(id=widget.id)

        elif action_type == "add_to_cart":
            await add_to_cart(context["user_id"], payload["product_id"])

            yield ClientEffectEvent(
                type="toast",
                payload={"message": "Added to cart!", "type": "success"},
            )
```
