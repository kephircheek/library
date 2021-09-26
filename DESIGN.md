## Models
### Item
- `id` (uuid):
- `mode` (enum): ['wish', '?todo', '?note']?
- `user_id` (uuid): user's main list
- `created` (datetime): зачем?
- `modified` (datetime):
- `deadline` (datetime):
- `secret` (str):  /[a-zA-Z0-9]{32}/
- `title` (str): < 50:
- `link` (str): < 100 link
- `address` (str) < 100 contact details
- `cost` (unsigned int): complexity or cost
- `relevance` (bool): for example reserved or not
- `rating` (unsigned int): for example number of votes

### Project (Ordered Set)
- `id` (uuid):
- `mode` (enum): ['INVITATION', '?discussion', '?todolist', '?tag', '?event']
- `user_id` (uuid, Optional):
- `created` (datetime):
- `modified` (datetime):
- `secret` (str):
- `item_ids` (array):
- `title` (str, Optional): < 50
- `details` (str, Optional): < 500
- `deadline` (datetime, Optional):
- `archive` (Boolean): mark as done

### Session:
- `id`: (uuid)
- `user_id`: (uuid)
- `created`: (datetime)
- `timezone`:
- `secret`:
- `lists`: (array[uuid]) `master_id`
- `reserved_items`

### _[future]_ User
- `id` (uuid):
- `lists` (array): array of list ids
- `secret`:

### _[future]_ Message
- `id` (uuid):
- `target` (uuid):
- `ref` (uuid): reference to item, message and etc.
- `content` (str): < 500
