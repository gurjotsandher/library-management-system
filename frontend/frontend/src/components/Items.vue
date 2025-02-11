<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sketchy/bootstrap.min.css"
      />
      <div class="row">
        <div class="col-sm-12">
          <h1
            class="text-center bg-primary text-white"
            style="border-radius: 10px"
          >
            Library 📚
          </h1>
          <hr />
          <br />
          <!-- Alert Message -->
          <b-alert variant="success" v-show="showMessage" show>{{
            message
          }}</b-alert>
          <button
            type="button"
            class="btn btn-success btn-sm"
            v-b-modal.item-modal
          >
            Add Item
          </button>
          <br /><br />
          <table class="table table-hover">
            <!-- Table Head -->
            <thead>
              <tr>
                <!-- Table Header Cells -->
                <th scope="col">Title</th>
                <th scope="col">Genre</th>
                <th scope="col">Available?</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in items" :key="index">
                <td>{{ item.title }}</td>
                <td>{{ item.genre }}</td>
                <td>
                  <span v-if="item.available"> ✔️ </span>
                  <span v-else> ❌ </span>
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-info btn-sm"
                      v-b-modal.item-update-modal
                      @click="editItem(item)"
                    >
                      Update
                    </button>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteItem(item)"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <footer
            class="bg-primary text-white text-center"
            style="border-radius: 10px"
          >
            Copyright &copy; All Rights Reserved 2025
          </footer>
        </div>
      </div>
      <!-- First Modal -->
      <b-modal
        ref="addItemModal"
        id="item-modal"
        title="Add a new item"
        hide-backdrop
        hide-footer
      >
        <b-form @submit="onSubmit" @onreset="onReset" class="w-100">
          <b-form-group
            id="form-title-group"
            label="Title:"
            label-for="form-title-input"
          >
            <b-form-input
              id="form-title-input"
              type="text"
              v-model="addItemForm.title"
              required
              placeholder="Enter Item"
            >
            </b-form-input>
          </b-form-group>
        </b-form>
        <b-form @submit="onSubmit" @onreset="onReset" class="w-100">
          <b-form-group
            id="form-genre-group"
            label="Genre:"
            label-for="form-genre-input"
          >
            <b-form-input
              id="form-genre-input"
              type="text"
              v-model="addItemForm.genre"
              required
              placeholder="Enter Genre"
            >
            </b-form-input>
          </b-form-group>
          <!-- Checkbox -->
          <b-form-group id="form-available-group">
            <b-form-checkbox-group
              v-model="addItemForm.available"
              id="form-checks"
            >
              <b-form-checkbox value="true"> Available? </b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>

          <b-button type="submit" variant="outline-info">Submit</b-button>
          <b-button type="reset" variant="outline-danger">Reset</b-button>
        </b-form>
      </b-modal>

      <!-- Second Modal -->
      <b-modal
        ref="editItemModal"
        id="item-update-modal"
        title="Update"
        hide-backdrop
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
          <b-form-group
            id="form-title-edit-group"
            label="Title:"
            label-for="form-title-edit-input"
          >
            <b-form-input
              id="form-title-edit-input"
              type="text"
              v-model="editForm.title"
              required
              placeholder="Enter title"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-genre-edit-group"
            label="Genre:"
            label-for="form-genre-edit-input"
          >
            <b-form-input
              id="form-genre-edit-input"
              type="text"
              v-model="editForm.genre"
              required
              placeholder="Enter genre"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group id="form-available-edit-group">
            <b-form-checkbox-group
              v-model="editForm.available"
              id="form-checks"
            >
              <b-form-checkbox value="true">Available?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="outline-info">Update</b-button>
            <b-button type="reset" variant="outline-danger">Cancel</b-button>
          </b-button-group>
        </b-form>
      </b-modal>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      items: [],
      addItemForm: {
        title: "",
        genre: "",
        available: [],
      },
      editForm: {
        id: "",
        title: "",
        genre: "",
        available: [],
      },
      message: "",
      showMessage: false,
    };
  },
  methods: {
    // GET Function
    getItems() {
      const path = "http://localhost:5000/items";
      axios
        .get(path)
        .then((res) => {
          this.items = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    // POST function
    addItem(payLoad) {
      const path = "http://localhost:5000/items";
      axios
        .post(path, payLoad)
        .then(() => {
          this.getItems();
          this.message = "Item Added!";
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 3000);
        })
        .catch((err) => {
          console.error(err);
          this.getItems();
        });
    },
    initForm() {
      this.addItemForm.title = "";
      this.addItemForm.genre = "";
      this.addItemForm.available = [];
      this.editForm.id = "";
      this.editForm.title = "";
      this.editForm.genre = "";
      this.editForm.available = [];
    },
    onSubmit(e) {
      e.preventDefault();
      this.$refs.addItemModal.hide();
      let available = false;
      if (this.addItemForm.available[0]) available = true;
      const payload = {
        title: this.addItemForm.title,
        genre: this.addItemForm.genre,
        available,
      };
      this.addItem(payload);
      this.initForm();
    },
    //  This is for Modal 1 to reset the item values
    onReset(e) {
      e.preventDefault();
      this.$refs.addItemModal.hide();
      this.initForm();
    },
    //  This is for Modal 2 to submit updated item
    onSubmitUpdate(e) {
      e.preventDefault();
      this.$refs.editItemModal.hide();
      let available = false;
      if (this.editForm.available[0]) available = true;
      const payload = {
        title: this.editForm.title,
        genre: this.editForm.genre,
        available,
      };
      this.updateItem(payload, this.editForm.id);
    },

    // Handle cancel button click

    onResetUpdate(e) {
      e.preventDefault();
      this.$refs.addItemModal.hide();
      this.initForm();
      this.getItems();
    },

    // Update Individual Item
    updateItem(payload, itemId) {
      const path = `http://localhost:5000/items/${itemId}`;
      axios
        .put(path, payload)
        .then((res) => {
          console.log("Response from the server", res.data);
          this.getItems();
          this.message = "Item Updated!";
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 3000);
        })
        .catch((err) => {
          console.error(err);
          this.getItems();
        });
    },
    // Delete Individual Item
    removeItem(itemId) {
      const path = `http://localhost:5000/items/${itemId}`;
      axios
        .delete(path)
        .then(() => {
          this.getItems();
          this.message = "Item Removed 🗑️!";
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 3000);
        })
        .catch((err) => {
          console.error(err);
          this.getItems();
        });
    },

    // Handle update button
    editItem(item) {
      this.editForm = item;
    },

    // Handle delete button
    deleteItem(item) {
      this.removeItem(item.id);
    },
  },
  created() {
    console.log("Component is being created!");
    this.getItems();
  }
};
</script>
