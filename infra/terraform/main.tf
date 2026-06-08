# Minimal Azure scaffold for the platform. Fill in subscription and naming,
# then terraform init && terraform apply.
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-agentic-rag"
  location = "westeurope"
}

resource "azurerm_cognitive_account" "openai" {
  name                = "agentic-rag-openai"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "OpenAI"
  sku_name            = "S0"
}
