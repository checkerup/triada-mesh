# Triada Custom KeyPool Providers

Triada uses an open provider architecture to decouple the core Watchdog & Perpetual Relay engine from credential sources.

## How it works

The core engine relies on `KeyPoolProvider` (defined in `triada.providers.base`):

```python
class KeyPoolProvider(ABC):
    @abstractmethod
    def get_key(self) -> str:
        """Returns an active, unexhausted API key."""
        pass

    @abstractmethod
    def report_exhausted(self, key: str) -> None:
        """Reports an API key as exhausted (401/402/429) for rotation."""
        pass

    @abstractmethod
    def available_keys_count(self) -> int:
        """Returns the number of active keys."""
        pass
```

## Built-in Provider: `env`

By default, Triada uses `EnvKeyPoolProvider`, which reads keys from the environment variable:

```bash
export TRIADA_JEV_API_KEY="sk-key1,sk-key2"
```

## Connecting an External / Private Provider

To connect a custom provider (e.g. an automated token farm, rotation microservice, or secure vault):

1. Implement a class inheriting from `KeyPoolProvider`:
   ```python
   from triada.providers.base import KeyPoolProvider

   class MyDynamicFarmProvider(KeyPoolProvider):
       def get_key(self) -> str:
           # Request fresh key from internal daemon or microservice
           return fetch_token_from_farm()
       ...
   ```
2. Configure it in `config.json` or via environment variable:
   ```json
   {
     "jev_provider": "my_package.module:MyDynamicFarmProvider"
   }
   ```
   Or:
   ```bash
   export TRIADA_JEV_PROVIDER="my_package.module:MyDynamicFarmProvider"
   ```

This architecture guarantees that proprietary account-generation farms or confidential credentials remain completely isolated in separate, private repositories while Triada remains 100% open-source and clean.
