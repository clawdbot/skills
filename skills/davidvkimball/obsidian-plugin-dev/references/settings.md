# Settings UI Pattern

Complete implementation of the Obsidian settings tab pattern.

## Settings Interface & Defaults

```typescript
// src/settings.ts
import { App, PluginSettingTab, Setting } from 'obsidian';
import MyPlugin from './main';

export interface MyPluginSettings {
  mySetting: string;
  enableFeature: boolean;
  selectedOption: 'option1' | 'option2' | 'option3';
  numericValue: number;
}

export const DEFAULT_SETTINGS: MyPluginSettings = {
  mySetting: 'default',
  enableFeature: true,
  selectedOption: 'option1',
  numericValue: 10,
};
```

## Settings Tab Implementation

```typescript
export class MyPluginSettingTab extends PluginSettingTab {
  plugin: MyPlugin;

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    // Section heading
    containerEl.createEl('h2', { text: 'My Plugin Settings' });

    // Text input
    new Setting(containerEl)
      .setName('Text setting')
      .setDesc('Enter a value')
      .addText(text => text
        .setPlaceholder('Enter value')
        .setValue(this.plugin.settings.mySetting)
        .onChange(async (value) => {
          this.plugin.settings.mySetting = value;
          await this.plugin.saveSettings();
        }));

    // Toggle
    new Setting(containerEl)
      .setName('Enable feature')
      .setDesc('Turn this feature on or off')
      .addToggle(toggle => toggle
        .setValue(this.plugin.settings.enableFeature)
        .onChange(async (value) => {
          this.plugin.settings.enableFeature = value;
          await this.plugin.saveSettings();
        }));

    // Dropdown
    new Setting(containerEl)
      .setName('Select option')
      .setDesc('Choose from available options')
      .addDropdown(dropdown => dropdown
        .addOption('option1', 'Option 1')
        .addOption('option2', 'Option 2')
        .addOption('option3', 'Option 3')
        .setValue(this.plugin.settings.selectedOption)
        .onChange(async (value: 'option1' | 'option2' | 'option3') => {
          this.plugin.settings.selectedOption = value;
          await this.plugin.saveSettings();
        }));

    // Slider
    new Setting(containerEl)
      .setName('Numeric value')
      .setDesc('Adjust the value (1-100)')
      .addSlider(slider => slider
        .setLimits(1, 100, 1)
        .setValue(this.plugin.settings.numericValue)
        .setDynamicTooltip()
        .onChange(async (value) => {
          this.plugin.settings.numericValue = value;
          await this.plugin.saveSettings();
        }));

    // Button
    new Setting(containerEl)
      .setName('Reset settings')
      .setDesc('Restore default values')
      .addButton(button => button
        .setButtonText('Reset')
        .setWarning()
        .onClick(async () => {
          this.plugin.settings = { ...DEFAULT_SETTINGS };
          await this.plugin.saveSettings();
          this.display(); // Refresh UI
        }));

    // Text area (multi-line)
    new Setting(containerEl)
      .setName('Notes')
      .setDesc('Enter multiple lines of text')
      .addTextArea(text => text
        .setPlaceholder('Enter notes here...')
        .setValue(this.plugin.settings.notes || '')
        .onChange(async (value) => {
          this.plugin.settings.notes = value;
          await this.plugin.saveSettings();
        }));
  }
}
```

## Register in Main Plugin

```typescript
// src/main.ts
import { MyPluginSettingTab } from './settings';

export default class MyPlugin extends Plugin {
  async onload() {
    await this.loadSettings();
    this.addSettingTab(new MyPluginSettingTab(this.app, this));
  }
}
```

## Advanced: Conditional Settings

Show/hide settings based on other values:

```typescript
display(): void {
  const { containerEl } = this;
  containerEl.empty();

  new Setting(containerEl)
    .setName('Enable advanced mode')
    .addToggle(toggle => toggle
      .setValue(this.plugin.settings.advancedMode)
      .onChange(async (value) => {
        this.plugin.settings.advancedMode = value;
        await this.plugin.saveSettings();
        this.display(); // Re-render to show/hide dependent settings
      }));

  // Only show if advanced mode is enabled
  if (this.plugin.settings.advancedMode) {
    new Setting(containerEl)
      .setName('Advanced option')
      .setDesc('Only visible in advanced mode')
      .addText(text => text
        .setValue(this.plugin.settings.advancedOption)
        .onChange(async (value) => {
          this.plugin.settings.advancedOption = value;
          await this.plugin.saveSettings();
        }));
  }
}
```

## Settings Migration

Handle settings changes between versions:

```typescript
async loadSettings() {
  const data = await this.loadData();
  this.settings = Object.assign({}, DEFAULT_SETTINGS, data);
  
  // Migrate old settings
  if (data?.oldSettingName !== undefined) {
    this.settings.newSettingName = data.oldSettingName;
    delete (this.settings as any).oldSettingName;
    await this.saveSettings();
  }
}
```
